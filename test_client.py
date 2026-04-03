from app import app, health

with app.test_client() as client:
    response = client.get('/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json}")

import os
print(f"\nFile HEALTH_RAN.txt exists: {os.path.exists('HEALTH_RAN.txt')}")
if os.path.exists('HEALTH_RAN.txt'):
    with open('HEALTH_RAN.txt') as f:
        print(f"File contents:\n{f.read()}")
