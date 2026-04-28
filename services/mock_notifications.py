"""
Mock Notification Service
Stubs for SMS, WhatsApp, and OTP delivery.
Replace the body of each function with real API calls (e.g. Twilio, MSG91, Fast2SMS).
"""
import random
import string
from datetime import datetime

# In-memory OTP store (use Redis in production)
_otp_store = {}


def generate_otp_mock(phone: str) -> str:
    """Generate a 6-digit OTP for a phone number and store it."""
    otp = ''.join(random.choices(string.digits, k=6))
    _otp_store[phone] = {
        'otp': otp,
        'generated_at': datetime.utcnow().isoformat(),
        'attempts': 0
    }
    print(f"[MOCK OTP] Phone: {phone} → OTP: {otp}")
    return otp


def verify_otp_mock(phone: str, otp: str) -> bool:
    """Verify OTP for a phone number. Always returns True in mock mode."""
    record = _otp_store.get(phone)
    if not record:
        # In mock mode, accept any 6-digit OTP
        return len(otp) == 6 and otp.isdigit()
    record['attempts'] += 1
    return record['otp'] == otp


def send_sms_mock(phone: str, message: str) -> dict:
    """
    Mock SMS sending. Logs locally and returns a mock confirmation object.
    Replace with: MSG91, Fast2SMS, Twilio, or any TRAI-compliant SMS gateway.
    """
    print(f"[MOCK SMS] To: {phone}")
    print(f"  Message: {message}")
    return {
        'success': True,
        'provider': 'MOCK_SMS_GATEWAY',
        'message_id': f"SMS_{random.randint(100000, 999999)}",
        'phone': phone,
        'status': 'delivered',
        'timestamp': datetime.utcnow().isoformat()
    }


def send_whatsapp_mock(phone: str, message: str, template: str = None) -> dict:
    """
    Mock WhatsApp message sending via Business API.
    Replace with: Meta WhatsApp Business API / Twilio WhatsApp.
    """
    print(f"[MOCK WHATSAPP] To: {phone}")
    print(f"  Template: {template or 'custom'}")
    print(f"  Message: {message}")
    return {
        'success': True,
        'provider': 'MOCK_WHATSAPP_API',
        'message_id': f"WA_{random.randint(100000, 999999)}",
        'phone': phone,
        'status': 'sent',
        'timestamp': datetime.utcnow().isoformat()
    }


def send_appointment_sms(phone: str, patient_name: str, facility_name: str,
                         appointment_date: str, appointment_id: int) -> dict:
    """Send a formatted appointment confirmation SMS."""
    message = (
        f"Dear {patient_name}, your appointment at {facility_name} is confirmed "
        f"on {appointment_date}. Appointment ID: #{appointment_id}. "
        f"Download your report at: https://vitalis.health/report/{appointment_id} "
        f"- Vitalis CIS"
    )
    return send_sms_mock(phone, message)


def send_reschedule_sms(phone: str, patient_name: str, facility_name: str,
                        new_date: str, appointment_id: int) -> dict:
    """Send a reschedule confirmation SMS."""
    message = (
        f"Dear {patient_name}, your appointment at {facility_name} has been "
        f"rescheduled to {new_date}. Ref ID: #{appointment_id}. "
        f"- Vitalis CIS"
    )
    return send_sms_mock(phone, message)


def send_credentials_sms(phone: str, facility_name: str, login_id: str,
                         password: str) -> dict:
    """Send facility login credentials via SMS."""
    message = (
        f"Welcome to Vitalis CIS! Your facility '{facility_name}' has been registered. "
        f"Login ID: {login_id} | Password: {password} "
        f"Login at: https://vitalis.health/login - Vitalis Team"
    )
    return send_sms_mock(phone, message)


def send_otp_sms(phone: str, otp: str) -> dict:
    """Send OTP verification SMS."""
    message = (
        f"Your Vitalis verification code is: {otp}. "
        f"Valid for 10 minutes. Do not share this code with anyone. "
        f"- Vitalis CIS"
    )
    return send_sms_mock(phone, message)
