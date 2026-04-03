from dotenv import load_dotenv
load_dotenv()

import os
import importlib

BACKUP_SERVICE_KEY = os.environ.get('BACKUP_SVC')
BACKUP_SERVICE_AVAILABLE = False

print(f"Step 1: BACKUP_SERVICE_KEY = {BACKUP_SERVICE_KEY[:20] if BACKUP_SERVICE_KEY else 'NOT SET'}")

if not BACKUP_SERVICE_KEY:
    print("Step 1 result: NO KEY, would return False")
else:
    print("Step 1 result: KEY EXISTS, continuing...")
    
    print(f"Step 2: BACKUP_SERVICE_AVAILABLE = {BACKUP_SERVICE_AVAILABLE}")
    if BACKUP_SERVICE_AVAILABLE:
        print("Step 2 result: Already cached, would return True")
    else:
        print("Step 2 result: Not cached, trying import...")
        
        try:
            print(f"Step 3: Attempting import...")
            mod = importlib.import_module(".".join(["google", "generativeai"]))
            print(f"Step 3 result: SUCCESS - module imported")
            BACKUP_SERVICE_AVAILABLE = True
            print(f"Final result: Would return True")
        except Exception as e:
            print(f"Step 3 result: FAILED - {type(e).__name__}: {e}")
            print(f"Final result: Would return False")

# Now test with the actual function
print("\n=== TESTING ACTUAL FUNCTION ===")
import sys
sys.path.insert(0, '.')
from app import ensure_backup_service_available
result = ensure_backup_service_available()
print(f"Function returned: {result}")
