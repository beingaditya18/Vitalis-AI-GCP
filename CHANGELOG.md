# Changelog

## Version 2.0.0 - Mobile Authentication System (2024)

### 🎉 Major Features Added

#### Authentication System Overhaul
- **Mobile-First Authentication**: Primary authentication via mobile number with OTP verification
- **Multi-Role Support**: Enhanced support for Patient, Doctor, ASHA Worker, Admin, and Facility roles
- **Dual Login Methods**: Users can login with Mobile + OTP or Mobile/Email + Password
- **OTP Verification**: Secure 6-digit OTP with 10-minute expiry and 3-attempt limit
- **Password Reset**: OTP-based password recovery system
- **Session Management**: Secure session handling with user context
- **Audit Logging**: Complete tracking of authentication events

### 📝 New Files Created

#### Core Authentication
- `services/auth_service.py` - Comprehensive authentication service with all auth logic
- `routes/auth.py` - Complete rewrite with new authentication endpoints
- `migrate_db.py` - Database migration script for existing installations
- `test_auth.py` - Comprehensive authentication test suite

#### Documentation
- `AUTH_GUIDE.md` - Complete authentication API documentation (300+ lines)
- `CHANGELOG.md` - This file, tracking all changes
- `setup.py` - Automated setup script for new installations

#### Updated Files
- `README.md` - Complete rewrite with authentication documentation
- `models.py` - Updated User, Patient, Doctor models; added OTPVerification model
- `services/mock_notifications.py` - Added `send_otp_sms()` function

### 🗄️ Database Schema Changes

#### Users Table (Updated)
- Added `mobile` VARCHAR(15) UNIQUE - Primary identifier
- Added `is_mobile_verified` BOOLEAN - Mobile verification status
- Added `is_email_verified` BOOLEAN - Email verification status
- Added `is_active` BOOLEAN - Account active status
- Added `last_login` DATETIME - Last login timestamp
- Changed `email` to nullable (mobile is primary)
- Changed `password_hash` to nullable (OTP-only login supported)

#### OTP Verifications Table (New)
```sql
CREATE TABLE otp_verifications (
    id INTEGER PRIMARY KEY,
    mobile VARCHAR(15) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    purpose VARCHAR(20) NOT NULL,  -- login, registration, password_reset
    is_verified BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Patients Table (Updated)
- Added `mobile` VARCHAR(15) - Duplicate for quick access

#### Doctors Table (Updated)
- Added `mobile` VARCHAR(15) - Duplicate for quick access

### 🔌 New API Endpoints

#### Authentication (`/api/auth`)
- `POST /otp/send` - Send OTP to mobile number
- `POST /otp/verify` - Verify OTP code
- `POST /register` - Register new user (all roles)
- `POST /login` - Login with OTP or password
- `POST /password/reset` - Reset password via OTP
- `GET /me` - Get current user profile
- `POST /logout` - Logout and clear session
- `POST /validate/mobile` - Check mobile availability
- `POST /validate/email` - Check email availability

### 🔒 Security Enhancements

- **Password Hashing**: PBKDF2 via Werkzeug (existing, maintained)
- **OTP Security**: Time-limited, attempt-limited, one-time use
- **Mobile Validation**: Indian mobile number format (10 digits, starts with 6-9)
- **Session Security**: Secure Flask sessions with user context
- **Audit Logging**: All authentication events logged with timestamps
- **Rate Limiting Ready**: Infrastructure for rate limiting in place

### 📚 Documentation Improvements

#### AUTH_GUIDE.md
- Complete API documentation with examples
- All endpoints documented with request/response formats
- Authentication flow diagrams
- Security features explained
- SMS gateway integration guide
- Frontend integration examples
- Troubleshooting guide
- Testing instructions

#### README.md
- Complete rewrite with authentication focus
- Quick start guide
- Installation instructions
- API endpoint reference
- Project structure overview
- Testing guide
- Deployment instructions
- Troubleshooting section

### 🧪 Testing

#### New Test Suite
- `test_auth.py` - Comprehensive authentication testing
  - Mobile validation tests
  - OTP send/verify flow tests
  - Registration tests (all roles)
  - Login tests (password and OTP)
  - Password reset tests
  - Automated test runner

### 🛠️ Developer Tools

#### Setup Script
- `setup.py` - Automated setup for new installations
  - Python version check
  - Dependency installation
  - Environment file creation
  - Directory creation
  - Database initialization
  - Next steps guide

#### Migration Script
- `migrate_db.py` - Safe database migration
  - Adds new columns to existing tables
  - Creates new tables
  - Preserves existing data
  - Rollback instructions

### 🔄 Migration Guide

For existing installations:

1. **Backup your database**
   ```bash
   cp instance/vitalis.db instance/vitalis.db.backup
   ```

2. **Pull latest code**
   ```bash
   git pull origin main
   ```

3. **Install new dependencies** (if any)
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migration script**
   ```bash
   python migrate_db.py
   ```

5. **Test authentication**
   ```bash
   python test_auth.py
   ```

### 📱 SMS Gateway Integration

#### Development
- Mock SMS service with console output
- OTP codes visible in console for testing
- No external dependencies required

#### Production
- Ready for integration with:
  - Twilio
  - MSG91
  - Fast2SMS
  - Any TRAI-compliant SMS gateway
- Integration examples in AUTH_GUIDE.md

### 🎯 Use Cases Supported

#### Patient Registration & Login
- Register with mobile number
- Verify mobile via OTP
- Login with mobile + OTP (passwordless)
- Login with mobile + password
- Reset password via OTP

#### Doctor Registration & Login
- Register with license number
- Mobile verification
- Professional profile creation
- Facility association

#### Facility Registration & Login
- Register facility with POC mobile
- Link facility to user account
- Manage facility profile
- OTP verification for facility

#### ASHA Worker Registration
- Register with assigned villages
- Mobile verification
- Community health management

### 🚀 Performance Improvements

- Optimized database queries with proper indexing
- Efficient OTP validation with attempt limiting
- Session management with minimal overhead
- Audit logging with async potential

### 🐛 Bug Fixes

- Fixed email uniqueness constraint (now nullable)
- Fixed password requirement (now optional for OTP-only)
- Fixed role-based redirects after login
- Fixed session management across roles

### ⚠️ Breaking Changes

#### Database Schema
- `users.email` is now nullable (migration handles this)
- `users.password_hash` is now nullable (migration handles this)
- New required field: `users.mobile` (migration adds this)

#### API Changes
- Old login endpoint behavior changed
- Now supports both OTP and password login
- Registration requires mobile number
- Email is now optional

#### Migration Required
- Existing installations MUST run `migrate_db.py`
- Or recreate database with new schema

### 📊 Statistics

- **New Files**: 7
- **Updated Files**: 4
- **New API Endpoints**: 9
- **New Database Tables**: 1
- **Updated Database Tables**: 3
- **Lines of Documentation**: 1000+
- **Test Cases**: 6 comprehensive test scenarios

### 🔮 Future Enhancements

Planned for future releases:

#### Authentication
- [ ] Two-factor authentication (2FA)
- [ ] Biometric authentication
- [ ] Social login (Google, Facebook)
- [ ] Email verification flow
- [ ] Device management
- [ ] Login history tracking
- [ ] Suspicious activity alerts

#### Platform
- [ ] Real-time notifications (WebSocket)
- [ ] Mobile app (React Native)
- [ ] Telemedicine video calls
- [ ] Multi-language support
- [ ] Offline mode
- [ ] WhatsApp integration
- [ ] Payment gateway

### 🙏 Acknowledgments

- Flask community for excellent framework
- Werkzeug for secure password hashing
- SQLAlchemy for robust ORM
- Google Gemini for AI capabilities

### 📞 Support

For issues or questions:
- Check AUTH_GUIDE.md for authentication help
- Check README.md for general documentation
- Run test_auth.py to verify setup
- Create GitHub issue for bugs

---

## Version 1.0.0 - Initial Release

### Features
- Patient dashboard with AI consultation
- Doctor dashboard with review system
- ASHA worker dashboard
- Admin dashboard with analytics
- Facility management
- CRM system
- Feedback module
- Google Gemini AI integration
- SQLite database
- Flask backend
- Bootstrap frontend

---

**For detailed authentication documentation, see [AUTH_GUIDE.md](AUTH_GUIDE.md)**
