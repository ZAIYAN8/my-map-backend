import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"DATABASE_URL loaded: {bool(DATABASE_URL)}")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM points")
    count = cur.fetchone()[0]
    print(f"数据库连接成功! 总点数: {count}")
    
    cur.execute("SELECT id, name, province FROM points LIMIT 3")
    rows = cur.fetchall()
    for row in rows:
        print(f"  ID={row[0]}, 名称={row[1]}, 省份={row[2]}")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"数据库连接失败: {e}")