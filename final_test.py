#!/usr/bin/env python
import requests
import json

print("Testing Banana Disease Classifier API...")
print("=" * 60)

r = requests.get('http://localhost:5000/health')
print(f"\n/health endpoint:")
print(f"  Status Code: {r.status_code}")
print(f"  Response: {json.dumps(r.json(), indent=2)}")

if r.status_code == 200:
    print("\n✅ API IS WORKING!")
else:
    print("\n❌ API returned error - but basic connectivity works")

print("\n" + "=" * 60)
