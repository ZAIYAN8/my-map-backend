import os
import uuid
import psycopg2
from functools import wraps
from flask import Flask, jsonify, request, send_from_directory, session, redirect, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
from qiniu import Auth, put_file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin123')

# 上传配置
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 七牛云配置
QINIU_ACCESS_KEY = os.environ.get('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = os.environ.get('QINIU_SECRET_KEY')
QINIU_BUCKET_NAME = os.environ.get('QINIU_BUCKET_NAME')
QINIU_BASE_URL = os.environ.get('QINIU_BASE_URL')

# 数据库配置
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

# ---------- 登录 ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect('/admin.html')
        else:
            return '<h1>用户名或密码错误</h1><a href="/login">返回登录</a>', 401
    return '''
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>管理员登录</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h2>运维后台登录</h2>
            <form method="post">
                <input type="text" name="username" placeholder="用户名" required><br><br>
                <input type="password" name="password" placeholder="密码" required><br><br>
                <button type="submit">登录</button>
            </form>
        </body>
        </html>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

# ---------- 公开接口 ----------
@app.route('/api/points')
def get_points():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(
                json_build_object(
                    'type', 'Feature',
                    'geometry', json_build_object(
                        'type', 'Point',
                        'coordinates', ARRAY[longitude, latitude]
                    ),
                    'properties', json_build_object(
                        'id', id,
                        'name', name,
                        'image_url', image_url,
                        'description', description,
                        'province', province,
                        'city', city
                    )
                )
            ), '[]'::json)
        ) FROM points;
    """)
    geojson = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify(geojson)

# ---------- 管理后台 API ----------
@app.route('/api/admin/points', methods=['GET'])
@admin_required
def admin_get_points():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, latitude, longitude, image_url, description, province, city FROM points ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    points = []
    for row in rows:
        points.append({
            'id': row[0],
            'name': row[1],
            'latitude': float(row[2]),
            'longitude': float(row[3]),
            'image_url': row[4],
            'description': row[5],
            'province': row[6],
            'city': row[7]
        })
    return jsonify(points)

@app.route('/api/admin/points', methods=['POST'])
@admin_required
def add_point():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO points (name, latitude, longitude, image_url, description, province, city)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (data['name'], data['latitude'], data['longitude'], data.get('image_url', ''),
          data.get('description', ''), data.get('province', ''), data.get('city', '')))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': new_id, 'message': '添加成功'}), 201

@app.route('/api/admin/points/<int:point_id>', methods=['PUT'])
@admin_required
def update_point(point_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE points SET name=%s, latitude=%s, longitude=%s, image_url=%s,
        description=%s, province=%s, city=%s WHERE id=%s
    """, (data['name'], data['latitude'], data['longitude'], data.get('image_url', ''),
          data.get('description', ''), data.get('province', ''), data.get('city', ''), point_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': '更新成功'})

@app.route('/api/admin/points/<int:point_id>', methods=['DELETE'])
@admin_required
def delete_point(point_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM points WHERE id = %s", (point_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': '删除成功'})

# ---------- 图片上传 ----------
@app.route('/api/upload', methods=['POST'])
@admin_required
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件类型'}), 400

    ext = file.filename.rsplit('.', 1)[1].lower()
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
    file.save(temp_path)

    try:
        q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
        token = q.upload_token(QINIU_BUCKET_NAME)
        ret, info = put_file(token, f'images/{new_filename}', temp_path)
        if ret is not None:
            image_url = QINIU_BASE_URL + f'images/{new_filename}'
            return jsonify({'image_url': image_url}), 200
        else:
            return jsonify({'error': f'上传到七牛云失败: {info}'}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# ---------- 静态页面服务 ----------
@app.route('/')
def index():
    return send_from_directory('.', 'portal.html') if os.path.exists('portal.html') else redirect('/map.html')

@app.route('/map.html')
def map_page():
    return send_from_directory('.', 'map.html')

@app.route('/admin.html')
def admin_page():
    if not session.get('logged_in'):
        return redirect('/login')
    return send_from_directory('.', 'admin.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if filename == 'admin.html':
        abort(403)
    if filename.endswith('.html') or filename.endswith('.js') or filename.endswith('.css'):
        return send_from_directory('.', filename)
    else:
        abort(403)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)