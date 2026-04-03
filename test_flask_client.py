from app import app

with app.test_client() as client:
    # Test /health
    response = client.get('/health')
    print(f"/health: Status {response.status_code}")
    if response.status_code == 200:
        print(f"  Response: {response.json}")
    else:
        print(f"  Error: {response.json}")
    
    # Test /info
    response = client.get('/info')
    print(f"\n/info: Status {response.status_code}")
    if response.status_code == 200:
        print(f"  external_available: {response.json.get('external_available')}")
