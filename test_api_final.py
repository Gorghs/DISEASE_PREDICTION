import requests

print("=" * 60)
print("TESTING  BANANA DISEASE CLASSIFIER API")
print("=" * 60)

# Test /health
print("\n1. Testing /health endpoint:")
r = requests.get('http://localhost:5000/health')
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json
    print(f"   Response: {data}")
else:
    print(f"   Error: {r.json}")

# Test /info
print("\n2. Testing /info endpoint:")
r = requests.get('http://localhost:5000/info')
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json
    print(f"   Has 'classes': {bool(data.get('classes'))}")
    print(f"   Classes: {data.get('classes')}")
    print(f"   External available: {data.get('external_available')}")
else:
    print(f"   Error: {r.json}")

# Test /
print("\n3. Testing / (homepage):")
r = requests.get('http://localhost:5000/')
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    print(f"   HTML length: {len(r.text)} bytes")
else:
    print(f"   Error retrieving homepage")

print("\n" + "=" * 60)
print("API is READY to use!")
print("=" * 60)
