import requests
import re
import base64
import json

s = requests.Session()

# Step 1: Get captcha
print("=== Step 1: Get captcha ===")
r = s.get('http://127.0.0.1:5000/api/captcha')
data = r.json()
svg_b64 = data['image'].split(',')[1]
svg_text = base64.b64decode(svg_b64).decode('utf-8')

# Extract captcha text from SVG text elements
matches = re.findall(r'>([A-Z0-9])<', svg_text)
captcha_text = ''.join(matches)
print(f"Captcha text extracted: '{captcha_text}' (length: {len(captcha_text)})")
print(f"SVG text sample: {svg_text[:500]}")

# Step 2: Login
print("\n=== Step 2: Login ===")
r = s.post('http://127.0.0.1:5000/api/auth/login', json={
    'username': 'admin',
    'password': 'your-strong-password',
    'captcha': captcha_text
})
print(f"Login response: {r.status_code} {r.json()}")

# Step 3: Check auth
print("\n=== Step 3: Check auth ===")
r = s.get('http://127.0.0.1:5000/api/auth/check')
print(f"Auth check: {r.json()}")

# Step 4: Get points
print("\n=== Step 4: Get points ===")
r = s.get('http://127.0.0.1:5000/api/points')
print(f"Points status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"Points type: {data.get('type')}")
    features = data.get('features', [])
    print(f"Features count: {len(features)}")
    if features:
        print(f"First feature: {json.dumps(features[0], indent=2, ensure_ascii=False)}")
else:
    print(f"Error: {r.text}")