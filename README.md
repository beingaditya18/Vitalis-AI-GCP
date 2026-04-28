# Vitalis AI - Rural Healthcare Intelligence System

## Overview

Vitalis AI is a comprehensive healthcare platform designed for rural India, featuring AI-powered diagnostics, appointment management, and a robust multi-role authentication system with mobile OTP verification.

## 🌟 Key Features

### 🔐 Advanced Authentication System
- **Mobile-First Authentication** with OTP verification
- **Multi-Role Support**: Patient, Doctor, ASHA Worker, Admin, Facility
- **Dual Login Methods**: Mobile/Email + Password or Mobile + OTP
- **Secure Password Reset** via OTP
- **Session Management** with comprehensive audit logging
- **Indian Mobile Number Validation** (10 digits, starts with 6-9)

### 👥 User Roles
- **Patient**: Book appointments, AI consultations, medical records
- **Doctor**: Review consultations, manage appointments, AI diagnostic tools
- **ASHA Worker**: Community health management, patient tracking
- **Admin**: System administration, analytics, reporting
- **Facility**: Healthcare facility management, doctor/service management

### 🏥 Core Healthcare Features
- AI-powered symptom analysis using Google Gemini
- Appointment scheduling and management
- Facility and doctor discovery
- Diagnostic service booking
- Patient feedback and CRM
- ABHA integration ready
- Geotagged facility registration
- Multi-modal file uploads (images, videos, PDFs)

### 🤖 AI-Powered Tools
- Clinical summarization
- Risk assessment
- SHAP explainability
- Visual intelligence
- RAG assistant
- Prescription engine
- Three-layer explanation system

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Navigate to project directory**
```bash
cd vitalis-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your configuration
```

Required environment variables:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///vitalis.db
GEMINI_API_KEY=your-gemini-api-key
```

5. **Initialize database**

For new installation:
```bash
python app.py  # This will create all tables
```

For existing database (migration):
```bash
python migrate_db.py
```

6. **Run the application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🔐 Authentication System

### Quick Test

Run the comprehensive authentication test suite:
```bash
python test_auth.py
```

This tests:
- ✅ Mobile number validation
- ✅ OTP send/verify flow
- ✅ User registration (all roles)
- ✅ Login with password
- ✅ Login with OTP
- ✅ Password reset

### Complete Documentation

See **[AUTH_GUIDE.md](AUTH_GUIDE.md)** for:
- Complete API documentation
- All endpoints with examples
- Request/response formats
- Authentication flows
- Security features
- Frontend integration examples
- SMS gateway integration
- Troubleshooting guide

### Quick API Examples

**Send OTP:**
```bash
curl -X POST http://localhost:5000/api/auth/otp/send \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543210", "purpose": "login"}'
```

**Register Patient:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "9876543210",
    "role": "patient",
    "name": "Rajesh Kumar",
    "password": "test123",
    "age": 35,
    "gender": "Male"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543210", "password": "test123"}'
```

## 📁 Project Structure

```
vitalis-ai/
├── app.py                      # Main application entry point
├── config.py                   # Configuration settings
├── models.py                   # Database models (updated with auth)
├── migrate_db.py              # Database migration script
├── test_auth.py               # Authentication test suite
├── AUTH_GUIDE.md              # Complete authentication documentation
├── requirements.txt           # Python dependencies
├── routes/                    # API route handlers
│   ├── auth.py               # Authentication endpoints (NEW)
│   ├── patient.py            # Patient endpoints
│   ├── doctor.py             # Doctor endpoints
│   ├── asha.py               # ASHA worker endpoints
│   ├── admin.py              # Admin endpoints
│   ├── facility.py           # Facility endpoints
│   ├── cis.py                # CIS endpoints
│   └── health.py             # Health check endpoints
├── services/                  # Business logic services
│   ├── auth_service.py       # Authentication service (NEW)
│   ├── gemini_service.py     # AI service integration
│   ├── mock_abha.py          # ABHA mock service
│   └── mock_notifications.py # SMS/notification service (updated)
├── templates/                 # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── patient_dashboard.html
│   ├── doctor_dashboard.html
│   ├── asha_dashboard.html
│   ├── admin_dashboard.html
│   ├── facility_dashboard.html
│   ├── crm_dashboard.html
│   ├── feedback_module.html
│   └── tools/                # AI tool templates
└── static/                    # Static assets
    ├── css/
    ├── js/
    ├── img/
    └── uploads/
```

## 🔌 API Endpoints

### Authentication (`/api/auth`)
- `POST /otp/send` - Send OTP to mobile
- `POST /otp/verify` - Verify OTP code
- `POST /register` - Register new user
- `POST /login` - Login (OTP or password)
- `POST /password/reset` - Reset password
- `GET /me` - Get current user profile
- `POST /logout` - Logout
- `POST /validate/mobile` - Check mobile availability
- `POST /validate/email` - Check email availability

### Patient (`/api/patient`)
- `GET /profile` - Get patient profile
- `POST /consultation` - Submit consultation
- `GET /consultations` - Get consultation history
- `POST /appointment` - Book appointment

### Doctor (`/api/doctor`)
- `GET /consultations` - Get pending consultations
- `POST /review` - Review consultation
- `GET /appointments` - Get appointments

### Facility (`/api/facility`)
- `GET /profile` - Get facility profile
- `POST /doctors` - Add doctor
- `POST /services` - Add service
- `GET /appointments` - Get appointments
- `POST /slots` - Manage appointment slots

### Admin (`/api/admin`)
- `GET /users` - Get all users
- `GET /facilities` - Get all facilities
- `GET /analytics` - Get analytics

### CIS (`/api/cis`)
- `POST /facility/register` - Register facility
- `GET /crm/cases` - Get CRM cases
- `POST /feedback` - Submit feedback

## 🗄️ Database Schema

### New/Updated Tables

**users** (Updated)
- `id`, `email`, `mobile` (NEW), `password_hash`
- `role`, `is_mobile_verified` (NEW), `is_email_verified` (NEW)
- `is_active` (NEW), `last_login` (NEW), `created_at`

**otp_verifications** (NEW)
- `id`, `mobile`, `otp_code`, `purpose`
- `is_verified`, `attempts`, `expires_at`, `created_at`

**patients** (Updated)
- Added `mobile` field for quick access

**doctors** (Updated)
- Added `mobile` field for quick access

See `models.py` for complete schema.

## 🔒 Security Features

- ✅ **Password Hashing**: PBKDF2 via Werkzeug
- ✅ **OTP Authentication**: 6-digit codes, 10-minute expiry
- ✅ **Rate Limiting**: Max 3 OTP attempts
- ✅ **Session Management**: Secure Flask sessions
- ✅ **Mobile Validation**: Indian number format (6-9 start)
- ✅ **Audit Logging**: All auth events tracked
- ✅ **CORS Protection**: Configurable origins
- ✅ **SQL Injection Prevention**: SQLAlchemy ORM

## 🧪 Testing

### Automated Testing

```bash
# Run authentication test suite
python test_auth.py
```

### Manual Testing

1. Start the server:
```bash
python app.py
```

2. Access dashboards:
- Home: `http://localhost:5000/`
- Login: `http://localhost:5000/api/auth/login`
- Patient: `http://localhost:5000/patient`
- Doctor: `http://localhost:5000/doctor`
- ASHA: `http://localhost:5000/asha`
- Admin: `http://localhost:5000/admin`
- Facility: `http://localhost:5000/facility`

3. Test registration and login flows for each role

### Testing Gemini AI Integration

1. Go to Patient Dashboard (`/patient`)
2. Fill out "New Consultation" form
3. Submit with valid `GEMINI_API_KEY`
4. AI summary will be generated
5. Check Doctor Dashboard (`/doctor`) to review

## 📱 SMS Gateway Integration

### Development (Mock)
The system uses mock SMS in development. Check console for OTP codes.

### Production Setup

Replace mock service in `services/mock_notifications.py` with real gateway:

**Supported Gateways:**
- Twilio
- MSG91
- Fast2SMS
- Any TRAI-compliant SMS gateway

See [AUTH_GUIDE.md](AUTH_GUIDE.md) for integration examples.

## 🚀 Deployment

### Render.com (Recommended)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository (auto-detects `render.yaml`)
4. Add environment variables:
   - `SECRET_KEY`
   - `GEMINI_API_KEY`
   - `SMS_GATEWAY_API_KEY` (production)
5. Deploy

### Other Platforms

Compatible with:
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- DigitalOcean App Platform
- Any Python/Flask hosting

**Note:** For production with SQLite, ensure persistent storage. Consider PostgreSQL for cloud deployments.

## 🔧 Configuration

### Environment Variables

```env
# Required
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///vitalis.db
GEMINI_API_KEY=your-gemini-api-key

# Optional (Production)
SMS_GATEWAY_API_KEY=your-sms-api-key
SMS_GATEWAY_SENDER_ID=VITALS
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm instance/vitalis.db
python app.py  # Recreates tables
```

### Migration Issues
```bash
# Run migration
python migrate_db.py

# If fails, backup and recreate
```

### OTP Not Working
- Check console for mock OTP
- Verify mobile format (10 digits, 6-9 start)
- Configure real SMS gateway for production

### Import Errors
```bash
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Change port in app.py or:
flask run --port 5001
```

## 📚 Documentation

- **[AUTH_GUIDE.md](AUTH_GUIDE.md)** - Complete authentication documentation
- **[models.py](models.py)** - Database schema reference
- **[routes/](routes/)** - API endpoint implementations
- **[services/](services/)** - Business logic services

## 🗺️ Roadmap

### Authentication Enhancements
- [ ] Two-factor authentication (2FA)
- [ ] Biometric authentication
- [ ] Social login (Google, Facebook)
- [ ] Email verification
- [ ] Device management

### Platform Features
- [ ] Real-time notifications (WebSocket)
- [ ] Mobile app (React Native)
- [ ] Telemedicine video calls
- [ ] AI model improvements
- [ ] Multi-language support (Hindi, regional)
- [ ] Offline mode support
- [ ] WhatsApp integration
- [ ] Payment gateway integration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 💬 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Refer to [AUTH_GUIDE.md](AUTH_GUIDE.md) for authentication help
- Check troubleshooting section above

## 🙏 Acknowledgments

- Google Gemini AI for clinical intelligence
- Flask community for excellent framework
- Rural healthcare workers for inspiration

---

**Built with ❤️ for Rural Healthcare in India**

**Version:** 2.0.0 (with Mobile Authentication)  
**Last Updated:** 2024
