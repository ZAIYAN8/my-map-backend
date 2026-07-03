"""
数据库迁移脚本：初始化多用户系统
运行方式：python init_users.py
"""
import os
import psycopg2
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin123')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# 1. 创建 users 表（如果不存在）
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        phone VARCHAR(20) UNIQUE,
        role VARCHAR(20) DEFAULT 'user',
        created_at TIMESTAMP DEFAULT NOW()
    );
""")
print("✅ users 表已就绪")

# 2. 检查管理员是否存在，不存在则创建
cur.execute("SELECT id FROM users WHERE username = %s", (ADMIN_USER,))
admin = cur.fetchone()
if admin:
    admin_id = admin[0]
    # 更新管理员密码（与 .env 保持同步）
    cur.execute("UPDATE users SET password_hash = %s, role = 'admin' WHERE id = %s",
                (generate_password_hash(ADMIN_PASS), admin_id))
    print(f"✅ 管理员账号已更新（ID={admin_id}）")
else:
    cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'admin') RETURNING id",
                (ADMIN_USER, generate_password_hash(ADMIN_PASS)))
    admin_id = cur.fetchone()[0]
    print(f"✅ 管理员账号已创建（ID={admin_id}）")

# 3. 给 points 表添加 user_id 字段（如果不存在）
cur.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name = 'points' AND column_name = 'user_id'
        ) THEN
            ALTER TABLE points ADD COLUMN user_id INTEGER REFERENCES users(id);
        END IF;
    END $$;
""")
print("✅ points.user_id 字段已就绪")

# 4. 将现有无主的 points 分配给管理员
cur.execute("UPDATE points SET user_id = %s WHERE user_id IS NULL", (admin_id,))
print(f"✅ 已将无主点位分配给管理员（ID={admin_id}）")

conn.commit()
cur.close()
conn.close()
print("\n🎉 多用户系统初始化完成！")