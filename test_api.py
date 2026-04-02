# ============================================================
#   TEST SCRIPT FOR BANANA LEAF DISEASE CLASSIFIER API
# ============================================================

import requests
import json
from pathlib import Path

# API URL (change if not running locally)
API_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing: /health endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_info():
    """Test info endpoint"""
    print("\n" + "="*60)
    print("Testing: /info endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{API_URL}/info")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_predict(image_path):
    """Test prediction endpoint with an image"""
    print("\n" + "="*60)
    print(f"Testing: /predict endpoint with {image_path}")
    print("="*60)
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{API_URL}/predict", files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🍌 BANANA LEAF DISEASE CLASSIFIER - API TEST SUITE")
    print("="*60)
    print(f"API URL: {API_URL}")
    print("Make sure the Flask server is running: python app.py")
    
    # Test health check
    test_health()
    
    # Test info
    test_info()
    
    # Test prediction (uncomment if you have test image)
    # test_predict("path/to/banana_leaf.jpg")
    
    print("\n" + "="*60)
    print("✅ Test suite complete!")
    print("="*60)
