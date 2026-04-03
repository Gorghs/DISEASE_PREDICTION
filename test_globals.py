from app import BACKUP_SERVICE_KEY, BACKUP_SERVICE_AVAILABLE
print(f"After import:")
print(f"  BACKUP_SERVICE_KEY = {bool(BACKUP_SERVICE_KEY)}")
print(f"  BACKUP_SERVICE_AVAILABLE = {BACKUP_SERVICE_AVAILABLE}")

# Now call the function
from app import ensure_backup_service_available
result = ensure_backup_service_available()
print(f"\nAfter calling ensure_backup_service_available():")
print(f"  Return value = {result}")

# Check the global again
from app import BACKUP_SERVICE_AVAILABLE as flag_after
print(f"  BACKUP_SERVICE_AVAILABLE = {flag_after}")
