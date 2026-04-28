# Vitalis AI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup (First Time Only)

```bash
# Navigate to project
cd vitalis-ai

# Run automated setup
python setup.py

# OR manual setup:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Start Server

```bash
python app.py
```

Server runs at: `http://localhost:5000`

### 3. Test Authentication

```bash
# In another terminal
python test_auth.py
```

---

## 📱 Quick API Reference

### Send OTP
```bash
curl -X POST http://localhost:5000/api/auth/otp/send \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543210", "purpose": "login"}'
```

### Register Patient
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "9876543210",
    "role": "patient",
    "name": "Test Patient",
    "password": "test123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543210", "password": "test123"}'
```

---

## 🎭 User Roles

| Role | Description | Dashboard URL |
|------|-------------|---------------|
| **Patient** | Book appointments, AI consultations | `/patient` |
| **Doctor** | Review cases, manage appointments | `/doctor` |
| **ASHA** | Community health worker | `/asha` |
| **Admin** | System administration | `/admin` |
| **Facility** | Healthcare facility management | `/facility` |

---

## 🔑 Test Accounts

Create test accounts for each role:

```bash
# Patient
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543210", "role": "patient", "name": "Test Patient", "password": "test123"}'

# Doctor
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543211", "role": "doctor", "name": "Dr. Test", "specialty": "General", "license_number": "TEST123", "password": "test123"}'

# Facility
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"mobile": "9876543212", "role": "facility", "name": "Test Hospital", "facility_id": 1, "password": "test123"}'
```

---

## 🔧 Common Tasks

### Reset Database
```bash
rm instance/vitalis.db
python app.py
```

### Migrate Existing Database
```bash
python migrate_db.py
```

### Run Tests
```bash
python test_auth.py
```

### Check Logs
```bash
# Server logs appear in terminal where you ran app.py
# OTP codes appear in console (development mode)
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **README.md** | Complete documentation |
| **AUTH_GUIDE.md** | Authentication API reference |
| **CHANGELOG.md** | Version history |
| **QUICK_START.md** | This file |

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
# Windows: netstat -ano | findstr :5000
# Mac/Linux: lsof -ti:5000 | xargs kill -9

# Or use different port
flask run --port 5001
```

### Import Errors
```bash
pip install -r requirements.txt --force-reinstall
```

### Database Errors
```bash
# Reset database
rm instance/vitalis.db
python app.py
```

### OTP Not Working
- Check console output for mock OTP
- Verify mobile format: 10 digits, starts with 6-9
- For production: configure SMS gateway

---

## 🎯 Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/my-feature
```

### 2. Make Changes
- Edit code
- Test locally
- Update documentation

### 3. Test
```bash
python test_auth.py
# Manual testing in browser
```

### 4. Commit
```bash
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
```

### 5. Create Pull Request
- Open PR on GitHub
- Request review
- Merge when approved

---

## 🚀 Deployment Checklist

### Before Deploying

- [ ] Update SECRET_KEY in .env
- [ ] Add GEMINI_API_KEY
- [ ] Configure SMS gateway (production)
- [ ] Test all endpoints
- [ ] Run test suite
- [ ] Update documentation
- [ ] Check security settings
- [ ] Enable HTTPS
- [ ] Set up monitoring
- [ ] Configure backups

### Render.com Deployment

1. Push to GitHub
2. Create Web Service on Render
3. Connect repository
4. Add environment variables
5. Deploy

---

## 💡 Tips

### Development
- Use mock OTP in development (check console)
- Test with multiple roles
- Check audit logs in database
- Use browser dev tools for debugging

### Production
- Configure real SMS gateway
- Use PostgreSQL instead of SQLite
- Enable rate limiting
- Set up monitoring
- Regular backups
- HTTPS only
- Secure SECRET_KEY

### Testing
- Run test_auth.py after changes
- Test all user roles
- Test OTP expiry
- Test password reset
- Test session management

---

## 📞 Getting Help

### Documentation
1. Check README.md
2. Check AUTH_GUIDE.md
3. Check this file

### Testing
1. Run test_auth.py
2. Check console logs
3. Check database

### Issues
1. Check troubleshooting section
2. Search existing issues
3. Create new issue with details

---

## 🎓 Learning Resources

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### SQLAlchemy
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

### Authentication
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT vs Sessions](https://stackoverflow.com/questions/43452896/authentication-jwt-usage-vs-session)

---

## ⚡ Quick Commands Reference

```bash
# Setup
python setup.py

# Start server
python app.py

# Test auth
python test_auth.py

# Migrate DB
python migrate_db.py

# Reset DB
rm instance/vitalis.db && python app.py

# Install deps
pip install -r requirements.txt

# Create venv
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate

# Deactivate venv
deactivate
```

---

**Need more details? Check [README.md](README.md) or [AUTH_GUIDE.md](AUTH_GUIDE.md)**
