"""
Authentication System Test Script
Tests all authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/auth"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_mobile_validation():
    """Test mobile number validation"""
    print("\n\n🔍 Testing Mobile Validation...")
    
    # Valid mobile
    response = requests.post(f"{BASE_URL}/validate/mobile", json={
        "mobile": "9876543210"
    })
    print_response("Valid Mobile Check", response)
    
    # Invalid mobile
    response = requests.post(f"{BASE_URL}/validate/mobile", json={
        "mobile": "5876543210"
    })
    print_response("Invalid Mobile Check", response)

def test_otp_flow():
    """Test OTP send and verify"""
    print("\n\n📱 Testing OTP Flow...")
    
    mobile = "9876543210"
    
    # Send OTP
    response = requests.post(f"{BASE_URL}/otp/send", json={
        "mobile": mobile,
        "purpose": "login"
    })
    print_response("Send OTP", response)
    
    if response.status_code == 200:
        otp = response.json().get('mock_otp')
        print(f"\n🔑 Mock OTP: {otp}")
        
        # Verify OTP
        response = requests.post(f"{BASE_URL}/otp/verify", json={
            "mobile": mobile,
            "otp": otp,
            "purpose": "login"
        })
        print_response("Verify OTP", response)
        
        return otp
    
    return None

def test_registration():
    """Test user registration"""
    print("\n\n📝 Testing User Registration...")
    
    # Patient registration
    response = requests.post(f"{BASE_URL}/register", json={
        "mobile": "9876543210",
        "role": "patient",
        "name": "Rajesh Kumar",
        "email": "rajesh@example.com",
        "password": "test123",
        "age": 35,
        "gender": "Male",
        "blood_group": "O+"
    })
    print_response("Patient Registration", response)
    
    # Doctor registration
    response = requests.post(f"{BASE_URL}/register", json={
        "mobile": "9876543211",
        "role": "doctor",
        "name": "Dr. Priya Sharma",
        "email": "priya@example.com",
        "password": "test123",
        "specialty": "Cardiology",
        "license_number": "MCI12345"
    })
    print_response("Doctor Registration", response)
    
    # Facility registration
    response = requests.post(f"{BASE_URL}/register", json={
        "mobile": "9876543212",
        "role": "facility",
        "name": "City Hospital",
        "email": "admin@cityhospital.com",
        "password": "test123",
        "facility_id": 1
    })
    print_response("Facility Registration", response)

def test_login_with_password():
    """Test login with password"""
    print("\n\n🔐 Testing Login with Password...")
    
    # Login with mobile + password
    response = requests.post(f"{BASE_URL}/login", json={
        "mobile": "9876543210",
        "password": "test123"
    })
    print_response("Login with Mobile + Password", response)
    
    # Login with email + password
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "rajesh@example.com",
        "password": "test123"
    })
    print_response("Login with Email + Password", response)

def test_login_with_otp():
    """Test login with OTP"""
    print("\n\n🔐 Testing Login with OTP...")
    
    mobile = "9876543210"
    
    # Send OTP
    response = requests.post(f"{BASE_URL}/otp/send", json={
        "mobile": mobile,
        "purpose": "login"
    })
    
    if response.status_code == 200:
        otp = response.json().get('mock_otp')
        print(f"🔑 Mock OTP: {otp}")
        
        # Login with OTP
        response = requests.post(f"{BASE_URL}/login", json={
            "mobile": mobile,
            "otp": otp
        })
        print_response("Login with Mobile + OTP", response)

def test_password_reset():
    """Test password reset"""
    print("\n\n🔄 Testing Password Reset...")
    
    mobile = "9876543210"
    
    # Send OTP for password reset
    response = requests.post(f"{BASE_URL}/otp/send", json={
        "mobile": mobile,
        "purpose": "password_reset"
    })
    
    if response.status_code == 200:
        otp = response.json().get('mock_otp')
        print(f"🔑 Mock OTP: {otp}")
        
        # Reset password
        response = requests.post(f"{BASE_URL}/password/reset", json={
            "mobile": mobile,
            "otp": otp,
            "new_password": "newtest123"
        })
        print_response("Password Reset", response)
        
        # Try login with new password
        response = requests.post(f"{BASE_URL}/login", json={
            "mobile": mobile,
            "password": "newtest123"
        })
        print_response("Login with New Password", response)

def run_all_tests():
    """Run all authentication tests"""
    print("\n" + "="*60)
    print("  VITALIS AI - AUTHENTICATION SYSTEM TESTS")
    print("="*60)
    print("\n⚠️  Make sure the Flask server is running on http://localhost:5000")
    print("⚠️  This will create test users in the database")
    
    input("\nPress Enter to continue...")
    
    try:
        # Test 1: Mobile Validation
        test_mobile_validation()
        
        # Test 2: OTP Flow
        test_otp_flow()
        
        # Test 3: Registration
        test_registration()
        
        # Test 4: Login with Password
        test_login_with_password()
        
        # Test 5: Login with OTP
        test_login_with_otp()
        
        # Test 6: Password Reset
        test_password_reset()
        
        print("\n\n" + "="*60)
        print("  ✅ ALL TESTS COMPLETED")
        print("="*60)
        print("\nCheck the responses above for any errors.")
        print("Review the Flask server logs for detailed information.")
        
    except requests.exceptions.ConnectionError:
        print("\n\n❌ ERROR: Could not connect to Flask server")
        print("Make sure the server is running: python app.py")
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")

if __name__ == '__main__':
    run_all_tests()
