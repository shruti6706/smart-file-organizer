"""Quick test to verify API functionality"""
import requests
import time
import subprocess
import sys

def test_api():
    """Test the API endpoint"""
    url = "http://localhost:8000/health"
    
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print("✓ API is running on port 8000")
            print(f"✓ Health check: {response.json()}")
            return True
    except requests.exceptions.ConnectionError:
        print("✗ API is not running on port 8000")
        print("\nTo start the API, run:")
        print("  python main.py --api")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    test_api()
