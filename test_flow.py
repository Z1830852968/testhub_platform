import os
import time
import requests

BASE_URL = 'http://localhost:8000/api'

session = requests.Session()

# 2. Login
r = session.post(f"{BASE_URL}/auth/login/", json={
    "username": "testuser",
    "password": "testpassword123"
})
print("Login:", r.status_code, r.text)
token = r.json().get('access')
session.headers.update({'Authorization': f'Bearer {token}'})

r = session.get(f"{BASE_URL}/projects/")
projects = r.json().get('results', r.json())
project_id = projects[0]['id']

# 4. Start Exploration Run
r = session.post(f"{BASE_URL}/explorations/runs/", json={
    "project": project_id
})
print("Start Run:", r.status_code, r.text)
run_id = r.json()['id']

# 5. Wait for it to complete or fail
print("Waiting for run to complete...")
for i in range(30):
    time.sleep(2)
    r = session.get(f"{BASE_URL}/explorations/runs/{run_id}/")
    data = r.json()
    print(f"Run Status: {data['status']}")
    if data['status'] in ['completed', 'failed', 'stopped']:
        break

print("Final Result:", r.json())

# 6. Check Features
r = session.get(f"{BASE_URL}/explorations/features/?run={run_id}")
print("Features:", r.status_code, r.text)
