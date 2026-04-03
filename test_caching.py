import requests
import time

for i in range(2):
    r = requests.get('http://localhost:5000/health')
    ext_avail = r.json().get('external_available')
    print(f'Call {i+1}: external_available = {ext_avail}')
    time.sleep(0.5)
