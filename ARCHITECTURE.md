# Vitalis AI - Authentication Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         VITALIS AI PLATFORM                      │
│                    Healthcare Intelligence System                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  Login Page  │  Register Page  │  Dashboards (5 Roles)          │
│  HTML/CSS/JS │  OTP Input      │  Patient │ Doctor │ ASHA       │
│              │  Form Validation│  Admin   │ Facility            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (Flask Routes)                    │
├─────────────────────────────────────────────────────────────────┤
│  /api/auth/*        │  /api/patient/*   │  /api/doctor/*        │
│  - otp/send         │  - profile        │  - consultations      │
│  - otp/verify       │  - consultation   │  - review             │
│  - register         │  - appointments   │  - appointments       │
│  - login            │                   │                       │
│  - password/reset   │  /api/facility/*  │  /api/admin/*         │
│  - logout           │  - profile        │  - users              │
│  - me               │  - doctors        │  - facilities         │
│  - validate/*       │  - services       │  - analytics          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  AuthService              │  GeminiService                       │
│  - validate_mobile()      │  - analyze_symptoms()                │
│  - generate_otp()         │  - generate_summary()                │
│  - send_otp()             │                                      │
│  - verify_otp()           │  NotificationService                 │
│  - register_user()        │  - send_otp_sms()                    │
│  - login_with_mobile()    │  - send_appointment_sms()            │
│  - login_with_email()     │  - send_credentials_sms()            │
│  - reset_password()       │                                      │
│  - get_user_profile()     │  ABHAService (Mock)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER (SQLAlchemy)                 │
├─────────────────────────────────────────────────────────────────┤
│  Users               │  OTPVerifications  │  Patients            │
│  - id                │  - id              │  - id                │
│  - mobile ⭐         │  - mobile          │  - user_id           │
│  - email             │  - otp_code        │  - name              │
│  - password_hash     │  - purpose         │  - mobile            │
│  - role              │  - is_verified     │  - age, gender       │
│  - is_mobile_verified│  - attempts        │  - blood_group       │
│  - is_active         │  - expires_at      │  - abha_number       │
│  - last_login        │                    │                      │
│                      │                    │                      │
│  Doctors             │  Facilities        │  AuditLogs           │
│  - id                │  - id              │  - id                │
│  - user_id           │  - user_id         │  - user_id           │
│  - name              │  - name            │  - action            │
│  - mobile            │  - license_number  │  - details           │
│  - specialty         │  - poc_mobile      │  - timestamp         │
│  - license_number    │  - otp_verified    │                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
├─────────────────────────────────────────────────────────────────┤
│  SMS Gateway         │  Google Gemini AI  │  ABHA (Future)       │
│  - Twilio            │  - gemini-1.5-flash│  - Health Records    │
│  - MSG91             │  - Clinical Summary│  - Patient ID        │
│  - Fast2SMS          │  - Risk Assessment │                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow Diagrams

### 1. Registration Flow

```
┌──────────┐                                                    ┌──────────┐
│  User    │                                                    │  System  │
└────┬─────┘                                                    └────┬─────┘
     │                                                               │
     │  1. Enter Mobile Number                                      │
     ├──────────────────────────────────────────────────────────────>
     │                                                               │
     │                    2. Validate Mobile Format                 │
     │                    3. Check if Mobile Exists                 │
     │                    4. Generate 6-digit OTP                   │
     │                    5. Store OTP in Database                  │
     │                    6. Send SMS via Gateway                   │
     │                                                               │
     │  7. OTP Sent (expires in 10 min)                             │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
     │  8. Enter OTP + Registration Details                         │
     │     (name, role, password, etc.)                             │
     ├──────────────────────────────────────────────────────────────>
     │                                                               │
     │                    9. Verify OTP                             │
     │                    10. Check Expiry & Attempts               │
     │                    11. Create User Account                   │
     │                    12. Create Role Profile                   │
     │                    13. Mark Mobile as Verified               │
     │                    14. Create Session                        │
     │                    15. Log Registration Event                │
     │                                                               │
     │  16. Registration Success + Auto Login                       │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
     │  17. Redirect to Role Dashboard                              │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
```

### 2. Login Flow (OTP)

```
┌──────────┐                                                    ┌──────────┐
│  User    │                                                    │  System  │
└────┬─────┘                                                    └────┬─────┘
     │                                                               │
     │  1. Enter Mobile Number                                      │
     ├──────────────────────────────────────────────────────────────>
     │                                                               │
     │                    2. Check if User Exists                   │
     │                    3. Generate OTP                           │
     │                    4. Send SMS                               │
     │                                                               │
     │  5. OTP Sent                                                 │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
     │  6. Enter OTP                                                │
     ├──────────────────────────────────────────────────────────────>
     │                                                               │
     │                    7. Verify OTP                             │
     │                    8. Check User Active Status               │
     │                    9. Update Last Login                      │
     │                    10. Create Session                        │
     │                    11. Log Login Event                       │
     │                                                               │
     │  12. Login Success                                           │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
     │  13. Redirect to Dashboard                                   │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
```

### 3. Login Flow (Password)

```
┌──────────┐                                                    ┌──────────┐
│  User    │                                                    │  System  │
└────┬─────┘                                                    └────┬─────┘
     │                                                               │
     │  1. Enter Mobile/Email + Password                            │
     ├──────────────────────────────────────────────────────────────>
     │                                                               │
     │                    2. Find User by Mobile/Email              │
     │                    3. Check User Active Status               │
     │                    4. Verify Password Hash                   │
     │                    5. Update Last Login                      │
     │                    6. Create Session                         │
     │                    7. Log Login Event                        │
     │                                                               │
     │  8. Login Success                                            │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
     │  9. Redirect to Dashboard                                    │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
```

### 4. Password Reset Flow

```
┌──────────┐                                                    ┌──────────┐
│  User    │                                                    │  System  │
└────┬─────┘                                                    └────┬─────┘
     │                                                               │
     │  1. Enter Mobile Number                                      │
     ├──────────────────────────────────────────────────────────────>
     │                                                               │
     │                    2. Generate OTP (purpose: password_reset) │
     │                    3. Send SMS                               │
     │                                                               │
     │  4. OTP Sent                                                 │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
     │  5. Enter OTP + New Password                                 │
     ├──────────────────────────────────────────────────────────────>
     │                                                               │
     │                    6. Verify OTP                             │
     │                    7. Hash New Password                      │
     │                    8. Update User Password                   │
     │                    9. Log Password Reset Event               │
     │                                                               │
     │  10. Password Reset Success                                  │
     <──────────────────────────────────────────────────────────────┤
     │                                                               │
     │  11. Login with New Password                                 │
     ├──────────────────────────────────────────────────────────────>
     │                                                               │
```

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Login   │  │ Register │  │ Password │  │Dashboard │        │
│  │  Form    │  │  Form    │  │  Reset   │  │  (5 Roles)│       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
└───────┼─────────────┼─────────────┼─────────────┼───────────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK ROUTES (auth.py)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  /login  │  │/register │  │/password │  │   /me    │        │
│  │          │  │          │  │  /reset  │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
└───────┼─────────────┼─────────────┼─────────────┼───────────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AUTH SERVICE (auth_service.py)                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  validate_mobile()  │  generate_otp()  │  send_otp()    │   │
│  │  verify_otp()       │  register_user() │  login_*()     │   │
│  │  reset_password()   │  get_user_profile()               │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────┬─────────────────┬─────────────────┬─────────────────────┘
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   DATABASE   │  │ NOTIFICATION │  │  AUDIT LOG   │
│   (SQLite)   │  │   SERVICE    │  │   SERVICE    │
│              │  │              │  │              │
│ - Users      │  │ - send_sms() │  │ - log_event()│
│ - OTPs       │  │ - send_otp() │  │              │
│ - Profiles   │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                             │
└─────────────────────────────────────────────────────────────────┘

Layer 1: INPUT VALIDATION
├─ Mobile Number Format (Regex: ^[6-9]\d{9}$)
├─ Email Format (RFC 5322)
├─ Password Strength (Optional)
└─ SQL Injection Prevention (SQLAlchemy ORM)

Layer 2: AUTHENTICATION
├─ OTP Verification
│  ├─ 6-digit random code
│  ├─ 10-minute expiry
│  ├─ 3 attempt limit
│  └─ One-time use
├─ Password Verification
│  ├─ PBKDF2 hashing
│  ├─ Salt per password
│  └─ Werkzeug implementation
└─ Session Management
   ├─ Secure cookies
   ├─ User ID + Role
   └─ Timeout ready

Layer 3: AUTHORIZATION
├─ Role-Based Access Control (RBAC)
│  ├─ Patient
│  ├─ Doctor
│  ├─ ASHA Worker
│  ├─ Admin
│  └─ Facility
└─ Session Validation
   ├─ Check user_id in session
   ├─ Verify user is active
   └─ Check role permissions

Layer 4: AUDIT & MONITORING
├─ Authentication Events
│  ├─ Registration
│  ├─ Login (success/failure)
│  ├─ Password reset
│  └─ Logout
├─ Timestamps
├─ User IDs
└─ Action Details

Layer 5: DATA PROTECTION
├─ Password Hashing (Never store plain text)
├─ OTP Expiry (Time-limited)
├─ Session Security (HTTP-only cookies)
└─ HTTPS (Production requirement)
```

---

## Database Schema Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE SCHEMA                             │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │    Users     │
                    ├──────────────┤
                    │ id (PK)      │
                    │ mobile (UQ)  │⭐
                    │ email (UQ)   │
                    │ password_hash│
                    │ role         │
                    │ is_mobile_   │
                    │   verified   │
                    │ is_active    │
                    │ last_login   │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┬───────────────┐
           │               │               │               │
           ▼               ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ Patients │   │ Doctors  │   │  ASHA    │   │Facilities│
    ├──────────┤   ├──────────┤   ├──────────┤   ├──────────┤
    │ id (PK)  │   │ id (PK)  │   │ id (PK)  │   │ id (PK)  │
    │ user_id  │   │ user_id  │   │ user_id  │   │ user_id  │
    │ name     │   │ name     │   │ name     │   │ name     │
    │ mobile   │   │ mobile   │   │ villages │   │ poc_mobile│
    │ age      │   │ specialty│   │ patients │   │ license  │
    │ gender   │   │ license  │   │ tasks    │   │ address  │
    │ abha_no  │   │ facility │   │          │   │ verified │
    └──────────┘   └──────────┘   └──────────┘   └──────────┘

    ┌──────────────────┐              ┌──────────────────┐
    │OTPVerifications  │              │   AuditLogs      │
    ├──────────────────┤              ├──────────────────┤
    │ id (PK)          │              │ id (PK)          │
    │ mobile           │              │ user_id (FK)     │
    │ otp_code         │              │ action           │
    │ purpose          │              │ target_id        │
    │ is_verified      │              │ details          │
    │ attempts         │              │ timestamp        │
    │ expires_at       │              │                  │
    └──────────────────┘              └──────────────────┘
```

---

## API Request/Response Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    API REQUEST FLOW                              │
└─────────────────────────────────────────────────────────────────┘

1. CLIENT REQUEST
   ↓
   POST /api/auth/login
   Content-Type: application/json
   {
     "mobile": "9876543210",
     "password": "test123"
   }

2. FLASK ROUTE (routes/auth.py)
   ↓
   @auth_bp.route('/login', methods=['POST'])
   def login():
       data = request.get_json()
       mobile = data.get('mobile')
       password = data.get('password')
       
3. AUTH SERVICE (services/auth_service.py)
   ↓
   result = AuthService.login_with_mobile(mobile, password=password)
   
4. VALIDATION
   ↓
   - Validate mobile format
   - Find user in database
   - Check if user is active
   - Verify password hash
   
5. DATABASE QUERY (models.py)
   ↓
   user = User.query.filter_by(mobile=mobile).first()
   check_password_hash(user.password_hash, password)
   
6. SESSION CREATION
   ↓
   session['user_id'] = user.id
   session['role'] = user.role
   
7. AUDIT LOGGING
   ↓
   log = AuditLog(
       user_id=user.id,
       action='USER_LOGIN',
       details=f'Mobile: {mobile}'
   )
   
8. RESPONSE
   ↓
   {
     "success": true,
     "message": "Login successful",
     "user": {
       "id": 1,
       "mobile": "9876543210",
       "role": "patient",
       "last_login": "2024-01-15T10:30:00"
     }
   }
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION DEPLOYMENT                         │
└─────────────────────────────────────────────────────────────────┘

                         ┌──────────────┐
                         │   INTERNET   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  HTTPS/SSL   │
                         │  (Port 443)  │
                         └──────┬───────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   LOAD BALANCER       │
                    │   (Render/AWS/etc)    │
                    └───────────┬───────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │  App Server  │ │  App Server  │ │  App Server  │
        │   Instance 1 │ │   Instance 2 │ │   Instance 3 │
        │              │ │              │ │              │
        │  Flask App   │ │  Flask App   │ │  Flask App   │
        │  + Gunicorn  │ │  + Gunicorn  │ │  + Gunicorn  │
        └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
               │                │                │
               └────────────────┼────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │  PostgreSQL  │ │  SMS Gateway │ │  Gemini AI   │
        │   Database   │ │  (Twilio/    │ │  (Google)    │
        │              │ │   MSG91)     │ │              │
        └──────────────┘ └──────────────┘ └──────────────┘
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY STACK                            │
└─────────────────────────────────────────────────────────────────┘

BACKEND
├─ Python 3.8+
├─ Flask 3.0.0 (Web Framework)
├─ SQLAlchemy 2.0.23 (ORM)
├─ Werkzeug 3.0.1 (Security)
├─ Gunicorn 21.2.0 (WSGI Server)
└─ python-dotenv 1.0.0 (Config)

DATABASE
├─ SQLite (Development)
└─ PostgreSQL (Production Recommended)

AUTHENTICATION
├─ PBKDF2 Password Hashing
├─ OTP Generation (Random 6-digit)
├─ Session Management (Flask Sessions)
└─ Mobile Validation (Regex)

EXTERNAL SERVICES
├─ SMS Gateway (Twilio/MSG91/Fast2SMS)
├─ Google Gemini AI (Clinical Intelligence)
└─ ABHA (Future Integration)

FRONTEND
├─ HTML5
├─ CSS3 (Glassmorphism Design)
├─ JavaScript (Vanilla)
├─ Bootstrap 5 (Admin Dashboard)
└─ Chart.js (Analytics)

DEPLOYMENT
├─ Render.com (Recommended)
├─ Heroku (Alternative)
├─ AWS Elastic Beanstalk (Alternative)
└─ Docker (Containerization Ready)
```

---

## File Structure

```
vitalis-ai/
│
├── app.py                          # Main application entry
├── config.py                       # Configuration
├── models.py                       # Database models ⭐
├── requirements.txt                # Dependencies
│
├── routes/                         # API Routes
│   ├── auth.py                    # Authentication ⭐ NEW
│   ├── patient.py
│   ├── doctor.py
│   ├── asha.py
│   ├── admin.py
│   ├── facility.py
│   ├── cis.py
│   └── health.py
│
├── services/                       # Business Logic
│   ├── auth_service.py            # Auth service ⭐ NEW
│   ├── gemini_service.py
│   ├── mock_abha.py
│   └── mock_notifications.py      # SMS service ⭐ UPDATED
│
├── templates/                      # HTML Templates
│   ├── login.html
│   ├── register.html
│   ├── patient_dashboard.html
│   ├── doctor_dashboard.html
│   ├── asha_dashboard.html
│   ├── admin_dashboard.html
│   ├── facility_dashboard.html
│   └── tools/
│
├── static/                         # Static Assets
│   ├── css/
│   ├── js/
│   ├── img/
│   └── uploads/
│
├── instance/                       # Database
│   └── vitalis.db
│
├── docs/                           # Documentation
│   ├── README.md                  # Main docs ⭐ UPDATED
│   ├── AUTH_GUIDE.md              # Auth guide ⭐ NEW
│   ├── QUICK_START.md             # Quick ref ⭐ NEW
│   ├── CHANGELOG.md               # Changes ⭐ NEW
│   ├── ARCHITECTURE.md            # This file ⭐ NEW
│   └── IMPLEMENTATION_SUMMARY.md  # Summary ⭐ NEW
│
└── scripts/                        # Utility Scripts
    ├── setup.py                   # Setup script ⭐ NEW
    ├── migrate_db.py              # Migration ⭐ NEW
    └── test_auth.py               # Tests ⭐ NEW
```

---

**For detailed implementation, see [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)**  
**For API documentation, see [AUTH_GUIDE.md](AUTH_GUIDE.md)**  
**For quick start, see [QUICK_START.md](QUICK_START.md)**
