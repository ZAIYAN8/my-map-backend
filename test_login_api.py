import requests
import base64
import io

BASE = 'http://localhost:5000'
s = requests.Session()

# 1. 先测试未登录状态
r = s.get(f'{BASE}/api/points')
print(f"未登录访问 /api/points: {r.status_code}")

# 2. 获取验证码
r = s.get(f'{BASE}/api/captcha')
print(f"获取验证码: {r.status_code}")
captcha_data = r.json()
print(f"验证码数据: {list(captcha_data.keys())}")

# 3. 直接用 test_login 方式登录（绕过验证码）
r = s.post(f'{BASE}/api/auth/login', json={
    'username': 'admin',
    'password': 'your-strong-password',
    'captcha': 'test'
})
print(f"登录结果: {r.status_code}, {r.json()}")

# 4. 检查登录状态
r = s.get(f'{BASE}/api/auth/check')
print(f"登录状态: {r.json()}")

# 5. 获取数据
r = s.get(f'{BASE}/api/points')
print(f"获取数据: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    features = data.get('features', [])
    print(f"共 {len(features)} 个点位:")
    for f in features:
        p = f.get('properties', {})
        print(f"  {p.get('name')} - {p.get('province')} {p.get('city')}")
else:
    print(f"获取失败: {r.text}")

# 6. 测试 admin 接口
r = s.get(f'{BASE}/api/admin/points')
print(f"\nAdmin 接口: {r.status_code}")
if r.status_code == 200:
    points = r.json()
    print(f"共 {len(points)} 个点位")
    for p in points:
        print(f"  ID={p['id']}, {p['name']}, {p.get('province')} {p.get('city')}")