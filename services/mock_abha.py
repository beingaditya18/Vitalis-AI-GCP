"""
Mock ABHA (Ayushman Bharat Health Account) Service
Generates realistic ABHA numbers per ABDM guidelines.
Replace with real ABDM APIs: https://sandbox.abdm.gov.in/docs
"""
import random
import string
from datetime import datetime


def generate_mock_abha(name: str = "Patient", dob: str = "1990-01-01",
                       gender: str = "M", phone: str = "9000000000") -> dict:
    """
    Generate a mock ABHA number and card data.
    Real ABHA numbers are 14-digit format: XX-XXXX-XXXX-XXXX
    """
    # Generate 14-digit ABHA number
    digits = ''.join(random.choices(string.digits, k=14))
    abha_number = f"{digits[:2]}-{digits[2:6]}-{digits[6:10]}-{digits[10:14]}"

    # Generate ABHA address (username@abdm)
    name_slug = name.lower().replace(" ", "").replace(".", "")[:8]
    rand_suffix = random.randint(10, 99)
    abha_address = f"{name_slug}{rand_suffix}@abdm"

    return {
        'abha_number': abha_number,
        'abha_address': abha_address,
        'name': name,
        'dob': dob,
        'gender': gender,
        'phone': phone,
        'issued_on': datetime.utcnow().strftime('%d-%m-%Y'),
        'valid_till': '2099-12-31',
        'health_id_status': 'ACTIVE',
        'kyc_verified': False,  # Full KYC requires Aadhaar/PAN OTP
        'abha_card_url': f"/api/cis/abha/card/{abha_number.replace('-', '')}",
        'disclaimer': (
            'This is a mock ABHA number generated for demonstration purposes. '
            'Real ABHA creation requires integration with the Ayushman Bharat '
            'Digital Mission (ABDM) API and valid identity verification.'
        )
    }


def generate_facility_login_id(facility_name: str, state_code: str = "MH") -> str:
    """Generate a unique login ID for a facility."""
    name_slug = ''.join(e for e in facility_name.upper() if e.isalnum())[:6]
    rand_num = random.randint(1000, 9999)
    return f"VIT-{state_code}-{name_slug}-{rand_num}"


def generate_temp_password() -> str:
    """Generate a secure temporary password for new facility accounts."""
    chars = string.ascii_letters + string.digits + "!@#$"
    return ''.join(random.choices(chars, k=10))
