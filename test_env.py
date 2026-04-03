#!/usr/bin/env python3
"""Test if .env is being loaded correctly."""

from dotenv import load_dotenv
load_dotenv()
import os

# Test 1: Check if BACKUP_SVC is set
key = os.environ.get('BACKUP_SVC')
print(f"BACKUP_SVC from os.environ: {key[:30] + '...' if key else 'NOT SET'}")

# Test 2: Try to import google.generativeai
try:
    import google.generativeai as genai
    print(f"google.generativeai: AVAILABLE (version info available)")
except ImportError as e:
    print(f"google.generativeai: IMPORT FAILED - {e}")

# Test 3: Test the specific import method used in app
import importlib
try:
    mod = importlib.import_module(".".join(["google", "generativeai"]))
    print(f"importlib module import: SUCCESS")
except Exception as e:
    print(f"importlib module import: FAILED - {e}")

# Test 4: Try to configure google.generativeai if key exists
if key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        print(f"google.generativeai.configure(): SUCCESS")
    except Exception as e:
        print(f"google.generativeai.configure(): FAILED - {e}")
