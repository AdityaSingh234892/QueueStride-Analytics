import requests
import json

# Test the backend API
def test_backend():
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        print("✅ Backend Health Check:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Test registration
        print("🔐 Testing Registration:")
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "testpass123",
            "role": "manager"
        }
        
        response = requests.post("http://localhost:8000/api/auth/register", json=register_data)
        print(f"Registration Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Registration successful")
        else:
            print(f"Registration response: {response.text}")
        print()
        
        # Test login
        print("🔑 Testing Login:")
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print("✅ Login successful")
            print(f"Token: {token[:20]}...")
            
            # Test protected endpoint
            print("\n📊 Testing Dashboard Analytics:")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get("http://localhost:8000/api/analytics/dashboard", headers=headers)
            print(f"Dashboard Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Dashboard data retrieved")
                print(f"Analytics: {response.json()}")
            else:
                print(f"Dashboard response: {response.text}")
        else:
            print(f"Login response: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Stock Monitoring System Backend")
    print("=" * 50)
    test_backend()
