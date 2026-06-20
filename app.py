import os
import uuid
import random
import string
import io
import base64
import psycopg2
from datetime import datetime, timezone
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

# ---------- 内存状态：追踪数据库新记录 ----------
# 记录上次统计时的最大 id 和对应时间，用于判断是否有新数据
_last_checked_max_id = None
_last_checked_time = None

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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login.html')

# ---------- 验证码生成 ----------
def generate_captcha_text(length=4):
    """生成随机验证码文本"""
    chars = string.ascii_uppercase + string.digits
    chars = chars.replace('O', '').replace('0', '').replace('I', '').replace('1', '').replace('L', '')
    return ''.join(random.choices(chars, k=length))

def generate_captcha_svg(text):
    """使用纯 SVG 生成验证码图片（无需 Pillow）"""
    width, height = 130, 42
    chars = list(text)
    bg_colors = ['#f0f4ff', '#fff0f0', '#f0fff0', '#fffff0', '#f0f0ff', '#fff5f0']
    bg = random.choice(bg_colors)
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    svg_parts.append(f'<rect width="{width}" height="{height}" fill="{bg}"/>')
    for _ in range(5):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        color = f'rgb({random.randint(120,200)},{random.randint(120,200)},{random.randint(120,200)})'
        svg_parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1"/>')
    for _ in range(30):
        cx, cy = random.randint(0, width), random.randint(0, height)
        r = random.randint(1, 2)
        color = f'rgb({random.randint(100,200)},{random.randint(100,200)},{random.randint(100,200)})'
        svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#e67e22', '#1abc9c', '#c0392b', '#2980b9']
    for i, char in enumerate(chars):
        x = 18 + i * 26
        y = random.randint(26, 34)
        color = random.choice(colors)
        rotate = random.randint(-20, 20)
        font_size = random.randint(22, 28)
        svg_parts.append(
            f'<text x="{x}" y="{y}" font-size="{font_size}" font-family="Arial,sans-serif" '
            f'font-weight="bold" fill="{color}" transform="rotate({rotate},{x},{y-8})">{char}</text>'
        )
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

@app.route('/api/captcha')
def get_captcha():
    """获取验证码图片"""
    captcha_text = generate_captcha_text()
    session['captcha'] = captcha_text.upper()
    svg_content = generate_captcha_svg(captcha_text)
    svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode()
    return jsonify({'image': f'data:image/svg+xml;base64,{svg_base64}'})

# ---------- 统一认证接口 ----------
@app.route('/api/auth/check')
def auth_check():
    """检查是否已登录"""
    return jsonify({'logged_in': bool(session.get('logged_in'))})

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """JSON 登录接口（用户名 + 密码 + 验证码）"""
    data = request.json or {}
    username = data.get('username', '')
    password = data.get('password', '')
    captcha = data.get('captcha', '').upper()
    expected_captcha = session.get('captcha', '')
    if not captcha or captcha != expected_captcha:
        return jsonify({'success': False, 'message': '验证码错误'}), 401
    session.pop('captcha', None)
    if username == ADMIN_USER and password == ADMIN_PASS:
        session['logged_in'] = True
        return jsonify({'success': True, 'message': '登录成功'})
    return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

# ---------- 公开接口（不需要登录） ----------
@app.route('/api/points')
@admin_required
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

# ---------- 省份统计接口（需要登录） ----------
@app.route('/api/points/stats')
@admin_required
def get_points_stats():
    """按省份统计点数"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            COALESCE(province, '未知') as province,
            COUNT(*) as count
        FROM points 
        GROUP BY province 
        ORDER BY count DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    total = sum(row[1] for row in rows)
    stats = [{'province': row[0], 'count': row[1]} for row in rows]
    
    return jsonify({
        'total': total,
        'stats': stats
    })

# ---------- 距离上次新增记录接口（需要登录） ----------
@app.route('/api/last-upload')
@admin_required
def get_last_upload():
    """
    通过数据库最大 id 判断是否有人新增了数据点。
    如果有新记录（max_id 增大），重置天数从0开始；
    如果没变化，累计上次新增至今的天数。
    """
    global _last_checked_max_id, _last_checked_time
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(MAX(id), 0) FROM points")
    current_max = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    now = datetime.now(timezone.utc)
    
    # 首次运行 / 初始化
    if _last_checked_max_id is None:
        _last_checked_max_id = current_max
        _last_checked_time = now
    
    # 如果最大 id 变大了，说明有新数据加入
    if current_max > _last_checked_max_id:
        _last_checked_max_id = current_max
        _last_checked_time = now
    
    days = (now - _last_checked_time).days
    
    return jsonify({
        'current_max_id': current_max,
        'days_since': days,
        'last_update_time': _last_checked_time.isoformat(),
        'has_upload': _last_checked_max_id > 0
    })

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
    return send_from_directory('.', 'map.html')

@app.route('/login.html')
def login_page():
    return send_from_directory('.', 'login.html')

@app.route('/map.html')
def map_page():
    return send_from_directory('.', 'map.html')

@app.route('/admin.html')
def admin_page():
    return send_from_directory('.', 'admin.html')

@app.route('/datav/')
def datav_index():
    return send_from_directory('datav', 'index.html')

@app.route('/datav/<path:filename>')
def datav_static(filename):
    # JS/CSS/图片等静态资源不拦截，页面路由都返回 index.html（SPA）
    return send_from_directory('datav', filename)

@app.route('/<path:filename>')
def serve_static(filename):
    if filename in ('admin.html', 'login.html'):
        abort(403)
    if filename.endswith('.html') or filename.endswith('.js') or filename.endswith('.css'):
        return send_from_directory('.', filename)
    else:
        abort(403)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)