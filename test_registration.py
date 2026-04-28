"""
Quick registration test script
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/auth"

def test_patient_registration():
    """Test patient registration"""
    print("\n📝 Testing Patient Registration...")
    
    payload = {
        "mobile": "9876543210",
        "role": "patient",
        "name": "Test Patient",
        "email": "patient@test.com",
        "password": "test123",
        "age": 30,
        "gender": "Male",
        "blood_group": "O+"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

def test_doctor_registration():
    """Test doctor registration"""
    print("\n📝 Testing Doctor Registration...")
    
    payload = {
        "mobile": "9876543211",
        "role": "doctor",
        "name": "Dr. Test",
        "email": "doctor@test.com",
        "password": "test123",
        "specialty": "General Medicine",
        "license_number": "TEST123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

def test_facility_registration():
    """Test facility registration"""
    print("\n📝 Testing Facility Registration...")
    
    payload = {
        "mobile": "9876543212",
        "role": "facility",
        "name": "Test Hospital",
        "email": "facility@test.com",
        "password": "test123",
        "license_number": "FAC123",
        "address": "123 Test Street",
        "district": "Test District"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

def test_asha_registration():
    """Test ASHA registration"""
    print("\n📝 Testing ASHA Registration...")
    
    payload = {
        "mobile": "9876543213",
        "role": "asha",
        "name": "Test ASHA",
        "email": "asha@test.com",
        "password": "test123",
        "assigned_villages": "Village1, Village2"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

if __name__ == '__main__':
    print("="*60)
    print("  REGISTRATION TEST SUITE")
    print("="*60)
    print("\n⚠️  Make sure server is running on http://localhost:5000")
    
    try:
        results = []
        results.append(("Patient", test_patient_registration()))
        results.append(("Doctor", test_doctor_registration()))
        results.append(("Facility", test_facility_registration()))
        results.append(("ASHA", test_asha_registration()))
        
        print("\n" + "="*60)
        print("  RESULTS")
        print("="*60)
        for role, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{role}: {status}")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("Make sure the server is running: python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
