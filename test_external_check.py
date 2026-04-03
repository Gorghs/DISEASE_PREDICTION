from dotenv import load_dotenv
load_dotenv()

import os
import importlib

key = os.environ.get('BACKUP_SVC')
print(f"API Key loaded: {bool(key)}")
if key:
    print(f"Key starts with: {key[:20]}...")

try:
    mod = importlib.import_module("google.generativeai")
    print(f"google.generativeai: Available")
except:
    print(f"google.generativeai: NOT available")

# Now test the actual function from app
from app import ensure_backup_service_available
result = ensure_backup_service_available()
print(f"ensure_backup_service_available() returned: {result}")
