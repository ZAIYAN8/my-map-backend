import os
import uuid
import random
import string
import io
import base64
import traceback
import logging
import psycopg2
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, jsonify, request, send_from_directory, session, redirect, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from qcloud_cos import CosConfig, CosS3Client
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# 上传配置
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 腾讯云 COS 配置
COS_SECRET_ID = os.environ.get('COS_SECRET_ID')
COS_SECRET_KEY = os.environ.get('COS_SECRET_KEY')
COS_BUCKET_NAME = os.environ.get('COS_BUCKET_NAME')
COS_REGION = os.environ.get('COS_REGION')
COS_BASE_URL = f'https://{COS_BUCKET_NAME}.cos.{COS_REGION}.myqcloud.com/'

# 初始化 COS 客户端
_cos_client = None
def get_cos_client():
    global _cos_client
    if _cos_client is None:
        config = CosConfig(Region=COS_REGION, SecretId=COS_SECRET_ID, SecretKey=COS_SECRET_KEY)
        _cos_client = CosS3Client(config)
    return _cos_client

# 数据库配置
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

# ---------- 内存状态 ----------
_last_checked_max_id = None
_last_checked_time = None

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------- 认证辅助 ----------

def get_current_user():
    """从 session 获取当前用户信息，未登录返回 None"""
    if session.get('logged_in'):
        return {
            'id': session.get('user_id'),
            'username': session.get('username'),
            'role': session.get('role', 'user')
        }
    return None

def get_current_user_id():
    """获取当前用户 ID，未登录返回 None"""
    return session.get('user_id') if session.get('logged_in') else None

def login_required(f):
    """需要登录"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """需要管理员角色"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            abort(401)
        if session.get('role') != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# 旧兼容别名
admin_required_alias = login_required  # 大多数接口只需登录

# ---------- 验证码 ----------
def generate_captcha_text(length=4):
    chars = string.ascii_uppercase + string.digits
    chars = chars.replace('O', '').replace('0', '').replace('I', '').replace('1', '').replace('L', '')
    return ''.join(random.choices(chars, k=length))

def generate_captcha_svg(text):
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
    captcha_text = generate_captcha_text()
    session['captcha'] = captcha_text.upper()
    svg_content = generate_captcha_svg(captcha_text)
    svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode()
    return jsonify({'image': f'data:image/svg+xml;base64,{svg_base64}'})

# ---------- 认证接口 ----------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login.html')

@app.route('/api/auth/check')
def auth_check():
    user = get_current_user()
    if user:
        return jsonify({
            'logged_in': True,
            'username': user['username'],
            'role': user['role'],
            'user_id': user['id']
        })
    return jsonify({'logged_in': False})

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    captcha = data.get('captcha', '').upper()
    expected_captcha = session.get('captcha', '')

    if not captcha or captcha != expected_captcha:
        return jsonify({'success': False, 'message': '验证码错误'}), 401
    session.pop('captcha', None)

    if not username or not password:
        return jsonify({'success': False, 'message': '请输入用户名和密码'}), 401

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, role FROM users WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row and check_password_hash(row[2], password):
        session['logged_in'] = True
        session['user_id'] = row[0]
        session['username'] = row[1]
        session['role'] = row[3]
        logger.info(f'用户登录: {row[1]} (role={row[3]})')
        return jsonify({'success': True, 'message': '登录成功', 'role': row[3]})

    return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

# ---------- 个人资料 ----------

@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    user_id = get_current_user_id()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, phone, role, created_at FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({'error': '用户不存在'}), 404
    return jsonify({
        'id': row[0],
        'username': row[1],
        'phone': row[2] or '',
        'role': row[3],
        'created_at': row[4].isoformat() if row[4] else None
    })

@app.route('/api/profile/password', methods=['POST'])
@login_required
def change_password():
    data = request.json or {}
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')

    if len(new_password) < 4:
        return jsonify({'success': False, 'message': '新密码至少4位'}), 400

    user_id = get_current_user_id()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()

    if not row or not check_password_hash(row[0], old_password):
        cur.close()
        conn.close()
        return jsonify({'success': False, 'message': '原密码错误'}), 400

    cur.execute("UPDATE users SET password_hash = %s WHERE id = %s",
                (generate_password_hash(new_password), user_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': '密码修改成功'})

@app.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.json or {}
    phone = data.get('phone', '').strip()
    user_id = get_current_user_id()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET phone = %s WHERE id = %s", (phone or None, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': '资料已更新'})

# ---------- 用户管理（管理员） ----------

@app.route('/api/users', methods=['GET'])
@admin_required
def list_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.username, u.phone, u.role, u.created_at,
               COALESCE(p.cnt, 0) as point_count
        FROM users u
        LEFT JOIN (
            SELECT user_id, COUNT(*) as cnt FROM points GROUP BY user_id
        ) p ON u.id = p.user_id
        ORDER BY u.id
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    users = []
    for row in rows:
        users.append({
            'id': row[0],
            'username': row[1],
            'phone': row[2] or '',
            'role': row[3],
            'created_at': row[4].isoformat() if row[4] else None,
            'point_count': row[5]
        })
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
@admin_required
def create_user():
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'user').strip()
    phone = data.get('phone', '').strip() or None

    if not username or len(username) < 2:
        return jsonify({'success': False, 'message': '用户名至少2个字符'}), 400
    if not password or len(password) < 4:
        return jsonify({'success': False, 'message': '密码至少4位'}), 400
    if role not in ('admin', 'user'):
        return jsonify({'success': False, 'message': '角色必须是 admin 或 user'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'success': False, 'message': '用户名已存在'}), 409

    cur.execute(
        "INSERT INTO users (username, password_hash, role, phone) VALUES (%s, %s, %s, %s) RETURNING id",
        (username, generate_password_hash(password), role, phone)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f'管理员创建用户: {username} (ID={new_id}, role={role})')
    return jsonify({'success': True, 'message': '用户创建成功', 'id': new_id}), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    data = request.json or {}
    conn = get_db_connection()
    cur = conn.cursor()

    if 'role' in data:
        role = data['role']
        if role not in ('admin', 'user'):
            cur.close(); conn.close()
            return jsonify({'success': False, 'message': '角色无效'}), 400
        cur.execute("UPDATE users SET role = %s WHERE id = %s", (role, user_id))

    if 'password' in data:
        pwd = data['password']
        if len(pwd) < 4:
            cur.close(); conn.close()
            return jsonify({'success': False, 'message': '密码至少4位'}), 400
        cur.execute("UPDATE users SET password_hash = %s WHERE id = %s",
                    (generate_password_hash(pwd), user_id))

    if 'phone' in data:
        cur.execute("UPDATE users SET phone = %s WHERE id = %s",
                    (data['phone'] or None, user_id))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': '用户信息已更新'})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    current_user_id = get_current_user_id()
    if user_id == current_user_id:
        return jsonify({'success': False, 'message': '不能删除自己'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    # 把该用户的点位转移给当前管理员
    cur.execute("UPDATE points SET user_id = %s WHERE user_id = %s", (current_user_id, user_id))
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f'删除用户 ID={user_id}，点位已转移给管理员')
    return jsonify({'success': True, 'message': '用户已删除，点位已转移给管理员'})

# ---------- 点位查询辅助 ----------

def _user_points_filter(cur):
    """
    在当前 cursor 上应用用户过滤。
    管理员看全部，普通用户只看自己的。
    返回 (filter_sql, params) 用于拼接到 WHERE 子句。
    """
    user = get_current_user()
    if user and user['role'] != 'admin':
        return ('AND p.user_id = %s', (user['id'],))
    return ('', ())

def _user_points_where():
    """返回用于 WHERE 的 SQL 片段和参数"""
    user = get_current_user()
    if user and user['role'] != 'admin':
        return ('WHERE p.user_id = %s', (user['id'],))
    return ('', ())

# ---------- 地图 API ----------

@app.route('/api/points')
@login_required
def get_points():
    where_sql, where_params = _user_points_where()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""
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
                ORDER BY id
            ), '[]'::json)
        ) FROM points p
        {where_sql.replace('WHERE p.', 'WHERE ').replace('WHERE', 'WHERE ') if where_sql else ''}
    """, where_params)
    geojson = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify(geojson)

# ---------- 统计 API ----------

@app.route('/api/points/stats')
@login_required
def get_points_stats():
    filter_sql, params = _user_points_where()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT
            COALESCE(province, '未知') as province,
            COUNT(*) as count
        FROM points p
        {filter_sql.replace('WHERE p.', 'WHERE ')}
        GROUP BY province
        ORDER BY count DESC
    """, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    total = sum(row[1] for row in rows)
    stats = [{'province': row[0], 'count': row[1]} for row in rows]
    return jsonify({'total': total, 'stats': stats})

@app.route('/api/last-upload')
@login_required
def get_last_upload():
    global _last_checked_max_id, _last_checked_time
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(MAX(id), 0) FROM points")
    current_max = cur.fetchone()[0]
    cur.close()
    conn.close()
    now = datetime.now(timezone.utc)
    if _last_checked_max_id is None:
        _last_checked_max_id = current_max
        _last_checked_time = now
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
@login_required
def admin_get_points():
    filter_sql, params = _user_points_where()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT p.id, p.name, p.latitude, p.longitude, p.image_url,
               p.description, p.province, p.city, p.user_id,
               COALESCE(u.username, '—') as owner_name
        FROM points p
        LEFT JOIN users u ON p.user_id = u.id
        {filter_sql.replace('WHERE p.', 'WHERE ')}
        ORDER BY p.id
    """, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    points = []
    for row in rows:
        points.append({
            'id': row[0], 'name': row[1],
            'latitude': float(row[2]), 'longitude': float(row[3]),
            'image_url': row[4], 'description': row[5] or '',
            'province': row[6] or '', 'city': row[7] or '',
            'user_id': row[8], 'owner_name': row[9]
        })
    return jsonify(points)

@app.route('/api/admin/points', methods=['POST'])
@login_required
def add_point():
    data = request.json
    user_id = get_current_user_id()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO points (name, latitude, longitude, image_url, description, province, city, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (data['name'], data['latitude'], data['longitude'], data.get('image_url', ''),
          data.get('description', ''), data.get('province', ''), data.get('city', ''), user_id))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': new_id, 'message': '添加成功'}), 201

@app.route('/api/admin/points/<int:point_id>', methods=['PUT'])
@login_required
def update_point(point_id):
    data = request.json
    user = get_current_user()
    conn = get_db_connection()
    cur = conn.cursor()
    # 非管理员只能更新自己的点位
    if user['role'] != 'admin':
        cur.execute("SELECT user_id FROM points WHERE id = %s", (point_id,))
        row = cur.fetchone()
        if not row or row[0] != user['id']:
            cur.close(); conn.close()
            return jsonify({'error': '无权操作此点位'}), 403
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
@login_required
def delete_point(point_id):
    user = get_current_user()
    conn = get_db_connection()
    cur = conn.cursor()
    if user['role'] != 'admin':
        cur.execute("SELECT user_id FROM points WHERE id = %s", (point_id,))
        row = cur.fetchone()
        if not row or row[0] != user['id']:
            cur.close(); conn.close()
            return jsonify({'error': '无权操作此点位'}), 403
    cur.execute("DELETE FROM points WHERE id = %s", (point_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': '删除成功'})

@app.route('/api/admin/points/<int:point_id>/clear-image', methods=['POST'])
@login_required
def clear_point_image(point_id):
    user = get_current_user()
    conn = get_db_connection()
    cur = conn.cursor()
    if user['role'] != 'admin':
        cur.execute("SELECT user_id FROM points WHERE id = %s", (point_id,))
        row = cur.fetchone()
        if not row or row[0] != user['id']:
            cur.close(); conn.close()
            return jsonify({'error': '无权操作此点位'}), 403
    cur.execute("UPDATE points SET image_url = '' WHERE id = %s", (point_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': '图片已清除'})

# ---------- COS 诊断 ----------

@app.route('/api/cos-diagnose')
@login_required
def cos_diagnose():
    result = {
        'configured': all([COS_SECRET_ID, COS_SECRET_KEY, COS_BUCKET_NAME, COS_REGION]),
        'bucket': COS_BUCKET_NAME,
        'region': COS_REGION,
        'base_url': COS_BASE_URL if COS_BUCKET_NAME else None,
        'secret_id_set': bool(COS_SECRET_ID),
        'secret_key_set': bool(COS_SECRET_KEY),
    }
    if result['configured']:
        try:
            cos_client = get_cos_client()
            response = cos_client.list_objects(Bucket=COS_BUCKET_NAME, MaxKeys=1)
            result['connection'] = 'ok'
            result['object_count'] = 'has_objects' if response.get('Contents') else 'empty'
        except Exception as e:
            result['connection'] = 'failed'
            result['error_type'] = type(e).__name__
            result['error_detail'] = str(e)[:500]
    return jsonify(result)

# ---------- 图片上传 ----------

@app.route('/api/upload', methods=['POST'])
@login_required
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

    cos_configured = all([COS_SECRET_ID, COS_SECRET_KEY, COS_BUCKET_NAME, COS_REGION])
    if cos_configured:
        try:
            cos_client = get_cos_client()
            cos_key = f'images/{new_filename}'
            cos_client.upload_file(Bucket=COS_BUCKET_NAME, Key=cos_key, LocalFilePath=temp_path)
            image_url = COS_BASE_URL + cos_key
            logger.info(f'COS 上传成功: {cos_key}')
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({'image_url': image_url}), 200
        except Exception as e:
            logger.error(f'COS 上传失败: {traceback.format_exc()}')
            logger.warning(f'COS 上传失败，降级为本地存储: {str(e)}')

    local_url = f'/local-images/{new_filename}'
    logger.info(f'使用本地存储: {new_filename}')
    return jsonify({'image_url': local_url}), 200

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
    return redirect('/datav/')

@app.route('/datav/')
def datav_index():
    return send_from_directory('datav', 'index.html')

@app.route('/datav/<path:filename>')
def datav_static(filename):
    return send_from_directory('datav', filename)

@app.route('/local-images/<path:filename>')
def serve_local_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/<path:filename>')
def serve_static(filename):
    if filename in ('login.html',):
        abort(403)
    if filename.endswith('.html') or filename.endswith('.js') or filename.endswith('.css'):
        return send_from_directory('.', filename)
    else:
        abort(403)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)