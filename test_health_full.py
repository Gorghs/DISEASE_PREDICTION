import requests
import json

r = requests.get('http://localhost:5000/health')
print(f'Status: {r.status_code}')
print(f'Response:')
print(json.dumps(r.json(), indent=2))
