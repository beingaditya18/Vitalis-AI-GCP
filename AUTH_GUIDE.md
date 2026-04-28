# Vitalis AI - Authentication System Guide

## Overview

The Vitalis AI platform now features a comprehensive authentication system with mobile OTP verification, supporting multiple user roles: **Patient**, **Doctor**, **ASHA Worker**, **Admin**, and **Facility**.

## Key Features

✅ **Mobile-First Authentication** - Primary authentication via mobile number  
✅ **OTP Verification** - Secure 6-digit OTP with 10-minute expiry  
✅ **Multi-Role Support** - Patient, Doctor, ASHA, Admin, Facility  
✅ **Dual Login Methods** - Mobile + OTP or Mobile/Email + Password  
✅ **Password Reset** - OTP-based password recovery  
✅ **Session Management** - Secure session handling  
✅ **Audit Logging** - Complete authentication activity tracking  

---

## User Roles

### 1. Patient
- Register with mobile number
- Book appointments
- Consult with AI assistant
- View medical records

### 2. Doctor
- Register with license number
- Review patient consultations
- Manage appointments
- Access AI diagnostic tools

### 3. ASHA Worker
- Community health worker role
- Manage assigned villages
- Track patient tasks
- Coordinate with facilities

### 4. Admin
- System administration
- User management
- Analytics and reporting

### 5. Facility
- Healthcare facility management
- Doctor and service management
- Appointment scheduling
- Patient tracking

---

## API Endpoints

### 1. Send OTP

**Endpoint:** `POST /api/auth/otp/send`

**Request Body:**
```json
{
  "mobile": "9876543210",
  "purpose": "login"
}
```

**Purpose Options:**
- `login` - For user login
- `registration` - For new user registration
- `password_reset` - For password recovery

**Response:**
```json
{
  "success": true,
  "message": "OTP sent to 9876543210",
  "otp_id": 123,
  "expires_in_minutes": 10,
  "mock_otp": "123456"
}
```

---

### 2. Verify OTP

**Endpoint:** `POST /api/auth/otp/verify`

**Request Body:**
```json
{
  "mobile": "9876543210",
  "otp": "123456",
  "purpose": "login"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid OTP",
  "attempts_remaining": 2
}
```

---

### 3. Register User

**Endpoint:** `POST /api/auth/register`

#### Patient Registration
```json
{
  "mobile": "9876543210",
  "role": "patient",
  "name": "Rajesh Kumar",
  "email": "rajesh@example.com",
  "password": "SecurePass123",
  "age": 35,
  "gender": "Male",
  "blood_group": "O+",
  "abha_number": "12345678901234",
  "emergency_contact": "9876543211"
}
```

#### Doctor Registration
```json
{
  "mobile": "9876543210",
  "role": "doctor",
  "name": "Dr. Priya Sharma",
  "email": "priya@example.com",
  "password": "SecurePass123",
  "specialty": "Cardiology",
  "license_number": "MCI12345",
  "facility_id": 1
}
```

#### ASHA Worker Registration
```json
{
  "mobile": "9876543210",
  "role": "asha",
  "name": "Sunita Devi",
  "email": "sunita@example.com",
  "password": "SecurePass123",
  "assigned_villages": "Village1, Village2, Village3"
}
```

#### Facility Registration
```json
{
  "mobile": "9876543210",
  "role": "facility",
  "name": "City Hospital",
  "email": "admin@cityhospital.com",
  "password": "SecurePass123",
  "facility_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "mobile": "9876543210",
    "email": "rajesh@example.com",
    "role": "patient",
    "is_mobile_verified": true,
    "is_active": true,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

### 4. Login

**Endpoint:** `POST /api/auth/login`

#### Login with Mobile + OTP
```json
{
  "mobile": "9876543210",
  "otp": "123456"
}
```

#### Login with Mobile + Password
```json
{
  "mobile": "9876543210",
  "password": "SecurePass123"
}
```

#### Login with Email + Password
```json
{
  "email": "rajesh@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "mobile": "9876543210",
    "email": "rajesh@example.com",
    "role": "patient",
    "is_mobile_verified": true,
    "last_login": "2024-01-15T10:35:00"
  }
}
```

---

### 5. Reset Password

**Endpoint:** `POST /api/auth/password/reset`

**Request Body:**
```json
{
  "mobile": "9876543210",
  "otp": "123456",
  "new_password": "NewSecurePass123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

---

### 6. Get Current User

**Endpoint:** `GET /api/auth/me`

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "mobile": "9876543210",
    "email": "rajesh@example.com",
    "role": "patient",
    "profile": {
      "name": "Rajesh Kumar",
      "age": 35,
      "gender": "Male",
      "blood_group": "O+",
      "abha_number": "12345678901234"
    }
  }
}
```

---

### 7. Logout

**Endpoint:** `POST /api/auth/logout` or `GET /api/auth/logout`

**Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

### 8. Validate Mobile

**Endpoint:** `POST /api/auth/validate/mobile`

**Request Body:**
```json
{
  "mobile": "9876543210"
}
```

**Response:**
```json
{
  "valid": true,
  "exists": true,
  "message": "Mobile number is already registered"
}
```

---

### 9. Validate Email

**Endpoint:** `POST /api/auth/validate/email`

**Request Body:**
```json
{
  "email": "rajesh@example.com"
}
```

**Response:**
```json
{
  "valid": true,
  "exists": false,
  "message": "Email is available"
}
```

---

## Authentication Flow

### Registration Flow

```
1. User enters mobile number
   ↓
2. Send OTP: POST /api/auth/otp/send
   ↓
3. User receives OTP via SMS
   ↓
4. User enters OTP and registration details
   ↓
5. Verify OTP: POST /api/auth/otp/verify
   ↓
6. Register: POST /api/auth/register
   ↓
7. User is logged in automatically
```

### Login Flow (OTP)

```
1. User enters mobile number
   ↓
2. Send OTP: POST /api/auth/otp/send
   ↓
3. User receives OTP via SMS
   ↓
4. User enters OTP
   ↓
5. Login: POST /api/auth/login
   ↓
6. Session created, redirect to dashboard
```

### Login Flow (Password)

```
1. User enters mobile/email and password
   ↓
2. Login: POST /api/auth/login
   ↓
3. Session created, redirect to dashboard
```

### Password Reset Flow

```
1. User enters mobile number
   ↓
2. Send OTP: POST /api/auth/otp/send (purpose: password_reset)
   ↓
3. User receives OTP via SMS
   ↓
4. User enters OTP and new password
   ↓
5. Reset Password: POST /api/auth/password/reset
   ↓
6. Password updated successfully
```

---

## Mobile Number Validation

**Format:** Indian mobile numbers (10 digits starting with 6-9)

**Valid Examples:**
- 9876543210
- 8765432109
- 7654321098
- 6543210987

**Invalid Examples:**
- 5876543210 (starts with 5)
- 98765432 (less than 10 digits)
- 98765432101 (more than 10 digits)

---

## OTP Configuration

- **OTP Length:** 6 digits
- **Expiry Time:** 10 minutes
- **Max Attempts:** 3 attempts per OTP
- **Rate Limiting:** Recommended in production

---

## Security Features

### Password Hashing
- Uses Werkzeug's `generate_password_hash` with PBKDF2
- Secure password storage

### OTP Security
- Time-limited validity (10 minutes)
- Attempt limiting (3 attempts)
- One-time use only
- Automatic invalidation after verification

### Session Management
- Flask session with secure cookies
- Session cleared on logout
- User ID and role stored in session

### Audit Logging
- All authentication events logged
- User registration, login, password reset tracked
- Timestamp and details recorded

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120) UNIQUE,
    mobile VARCHAR(15) UNIQUE,
    password_hash VARCHAR(256),
    role VARCHAR(20) NOT NULL,
    is_mobile_verified BOOLEAN DEFAULT FALSE,
    is_email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### OTP Verifications Table
```sql
CREATE TABLE otp_verifications (
    id INTEGER PRIMARY KEY,
    mobile VARCHAR(15) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    purpose VARCHAR(20) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Integration with SMS Gateway

### Production Setup

Replace the mock SMS service in `services/mock_notifications.py` with a real SMS gateway:

#### Option 1: Twilio
```python
from twilio.rest import Client

def send_otp_sms(phone, otp):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your Vitalis verification code is: {otp}",
        from_='+1234567890',
        to=f'+91{phone}'
    )
    return {'success': True, 'message_id': message.sid}
```

#### Option 2: MSG91
```python
import requests

def send_otp_sms(phone, otp):
    url = "https://api.msg91.com/api/v5/otp"
    payload = {
        "template_id": "your_template_id",
        "mobile": phone,
        "otp": otp
    }
    headers = {"authkey": "your_auth_key"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
```

#### Option 3: Fast2SMS
```python
import requests

def send_otp_sms(phone, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "route": "otp",
        "variables_values": otp,
        "numbers": phone
    }
    headers = {"authorization": "your_api_key"}
    response = requests.post(url, data=payload, headers=headers)
    return response.json()
```

---

## Testing

### Test User Accounts

Create test users for each role:

```bash
# Patient
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "9876543210",
    "role": "patient",
    "name": "Test Patient",
    "password": "test123"
  }'

# Doctor
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "9876543211",
    "role": "doctor",
    "name": "Dr. Test",
    "specialty": "General Medicine",
    "license_number": "TEST123",
    "password": "test123"
  }'

# Facility
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "9876543212",
    "role": "facility",
    "name": "Test Hospital",
    "facility_id": 1,
    "password": "test123"
  }'
```

### Test OTP Flow

```bash
# 1. Send OTP
curl -X POST http://localhost:5000/api/auth/otp/send \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543210", "purpose": "login"}'

# 2. Verify OTP (use the mock_otp from response)
curl -X POST http://localhost:5000/api/auth/otp/verify \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543210", "otp": "123456", "purpose": "login"}'

# 3. Login with OTP
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543210", "otp": "123456"}'
```

---

## Frontend Integration

### Example: Login Form with OTP

```javascript
// Send OTP
async function sendOTP() {
  const mobile = document.getElementById('mobile').value;
  
  const response = await fetch('/api/auth/otp/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mobile, purpose: 'login' })
  });
  
  const data = await response.json();
  if (data.success) {
    alert('OTP sent to ' + mobile);
    // Show OTP input field
    document.getElementById('otp-section').style.display = 'block';
  }
}

// Login with OTP
async function loginWithOTP() {
  const mobile = document.getElementById('mobile').value;
  const otp = document.getElementById('otp').value;
  
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mobile, otp })
  });
  
  const data = await response.json();
  if (data.success) {
    // Redirect based on role
    window.location.href = `/${data.user.role}`;
  } else {
    alert(data.error);
  }
}
```

---

## Best Practices

1. **Always verify OTP before registration/login**
2. **Use HTTPS in production**
3. **Implement rate limiting for OTP requests**
4. **Store sensitive data encrypted**
5. **Use environment variables for secrets**
6. **Enable CORS only for trusted domains**
7. **Implement session timeout**
8. **Add CAPTCHA for repeated failed attempts**
9. **Log all authentication events**
10. **Regular security audits**

---

## Troubleshooting

### Issue: OTP not received
- Check mock_notifications.py console output
- Verify mobile number format
- Check SMS gateway configuration

### Issue: OTP expired
- OTPs expire after 10 minutes
- Request a new OTP

### Issue: Invalid OTP
- Check for typos
- Maximum 3 attempts allowed
- Request a new OTP after max attempts

### Issue: User already exists
- Use login instead of registration
- Or use password reset if forgotten

---

## Future Enhancements

- [ ] Two-factor authentication (2FA)
- [ ] Biometric authentication
- [ ] Social login (Google, Facebook)
- [ ] Email verification
- [ ] Account recovery options
- [ ] Device management
- [ ] Login history
- [ ] Suspicious activity alerts

---

## Support

For issues or questions, contact the development team or refer to the main README.md file.
