import sys
sys.path.insert(0, '.')

print("Importing app...")
try:
    import app
    print("Checking if function exists...")
    if hasattr(app, 'ensure_backup_service_available'):
        print("Function exists! Calling it...")
        result = app.ensure_backup_service_available()
        print(f"Result: {result}")
    else:
        print("Function does NOT exist in app module")
        print(f"Available functions: {[x for x in dir(app) if not x.startswith('_')]}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
