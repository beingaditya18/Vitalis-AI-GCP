from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from models import db, User, Patient, Doctor, ASHAWorker, Facility
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# ──────────────────────────────────────────────
# FRONTEND ROUTES
# ──────────────────────────────────────────────

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Render login page"""
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """Render registration page"""
    return render_template('register.html')

# ──────────────────────────────────────────────
# OTP MANAGEMENT
# ──────────────────────────────────────────────

@auth_bp.route('/otp/send', methods=['POST'])
def send_otp():
    """
    Send OTP to mobile number
    Body: { "mobile": "9876543210", "purpose": "login|registration|password_reset" }
    """
    data = request.get_json()
    mobile = data.get('mobile')
    purpose = data.get('purpose', 'login')
    
    if not mobile:
        return jsonify({'success': False, 'error': 'Mobile number is required'}), 400
    
    result = AuthService.send_otp(mobile, purpose)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@auth_bp.route('/otp/verify', methods=['POST'])
def verify_otp():
    """
    Verify OTP code
    Body: { "mobile": "9876543210", "otp": "123456", "purpose": "login" }
    """
    data = request.get_json()
    mobile = data.get('mobile')
    otp_code = data.get('otp')
    purpose = data.get('purpose', 'login')
    
    if not mobile or not otp_code:
        return jsonify({'success': False, 'error': 'Mobile and OTP are required'}), 400
    
    result = AuthService.verify_otp(mobile, otp_code, purpose)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

# ──────────────────────────────────────────────
# REGISTRATION
# ──────────────────────────────────────────────

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register new user - Simple version
    """
    data = request.get_json() if request.is_json else request.form.to_dict()
    
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    role = data.get('role', 'patient')
    
    if not email or not password or not name:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Email, name, and password are required'}), 400
        return render_template('register.html'), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Email already registered'}), 400
        return render_template('register.html'), 400
    
    # Create user with simple fields
    from werkzeug.security import generate_password_hash
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        is_email_verified=False,
        is_active=True
    )
    db.session.add(user)
    db.session.flush()
    
    # Create role-specific profile with minimal data
    if role == 'patient':
        profile = Patient(user_id=user.id, name=name)
        db.session.add(profile)
    elif role == 'doctor':
        profile = Doctor(user_id=user.id, name=name)
        db.session.add(profile)
    elif role == 'asha':
        profile = ASHAWorker(user_id=user.id, name=name)
        db.session.add(profile)
    elif role == 'facility':
        profile = Facility(
            user_id=user.id,
            name=name,
            poc_name=name,
            is_active=True
        )
        db.session.add(profile)
    
    db.session.commit()
    
    # Set session for web requests
    if not request.is_json:
        session['user_id'] = user.id
        session['role'] = user.role
        
        # Redirect based on role
        if role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'asha':
            return redirect(url_for('asha_dashboard'))
        elif role == 'facility':
            return redirect(url_for('facility_dashboard'))
        else:
            return redirect(url_for('patient_dashboard'))
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201

# ──────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login with email + password - Simple version
    """
    data = request.get_json() if request.is_json else request.form.to_dict()
    
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # For demo purposes
    
    if not email or not password:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        return render_template('login.html'), 400
    
    # Find user by email
    from werkzeug.security import check_password_hash
    user = User.query.filter_by(email=email).first()
    
    if not user:
        if request.is_json:
            return jsonify({'success': False, 'error': 'User not found'}), 401
        return render_template('login.html'), 401
    
    if not user.is_active:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Account is deactivated'}), 401
        return render_template('login.html'), 401
    
    if not user.password_hash or not check_password_hash(user.password_hash, password):
        if request.is_json:
            return jsonify({'success': False, 'error': 'Invalid password'}), 401
        return render_template('login.html'), 401
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Set session
    session['user_id'] = user.id
    session['role'] = user.role
    
    # Redirect based on role for web requests
    if not request.is_json:
        role = user.role
        if role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'asha':
            return redirect(url_for('asha_dashboard'))
        elif role == 'facility':
            return redirect(url_for('facility_dashboard'))
        else:
            return redirect(url_for('patient_dashboard'))
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200

# ──────────────────────────────────────────────
# PASSWORD MANAGEMENT
# ──────────────────────────────────────────────

@auth_bp.route('/password/reset', methods=['POST'])
def reset_password():
    """
    Reset password using OTP
    Body: {
        "mobile": "9876543210",
        "otp": "123456",
        "new_password": "newpassword123"
    }
    """
    data = request.get_json()
    mobile = data.get('mobile')
    otp = data.get('otp')
    new_password = data.get('new_password')
    
    if not mobile or not otp or not new_password:
        return jsonify({
            'success': False, 
            'error': 'Mobile, OTP, and new password are required'
        }), 400
    
    result = AuthService.reset_password(mobile, otp, new_password)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

# ──────────────────────────────────────────────
# SESSION MANAGEMENT
# ──────────────────────────────────────────────

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logout and clear session"""
    session.clear()
    
    if request.method == 'GET' or not request.is_json:
        return redirect(url_for('index'))
    
    return jsonify({'success': True, 'message': 'Logout successful'})

@auth_bp.route('/me', methods=['GET'])
def get_me():
    """Get current user profile"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    result = AuthService.get_user_profile(user_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

# ──────────────────────────────────────────────
# VALIDATION ENDPOINTS
# ──────────────────────────────────────────────

@auth_bp.route('/validate/mobile', methods=['POST'])
def validate_mobile():
    """Check if mobile number is already registered"""
    data = request.get_json()
    mobile = data.get('mobile')
    
    if not mobile:
        return jsonify({'valid': False, 'error': 'Mobile number is required'}), 400
    
    if not AuthService.validate_mobile(mobile):
        return jsonify({'valid': False, 'error': 'Invalid mobile number format'}), 400
    
    user = User.query.filter_by(mobile=mobile).first()
    
    return jsonify({
        'valid': True,
        'exists': user is not None,
        'message': 'Mobile number is already registered' if user else 'Mobile number is available'
    })

@auth_bp.route('/validate/email', methods=['POST'])
def validate_email():
    """Check if email is already registered"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'valid': False, 'error': 'Email is required'}), 400
    
    if not AuthService.validate_email(email):
        return jsonify({'valid': False, 'error': 'Invalid email format'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    return jsonify({
        'valid': True,
        'exists': user is not None,
        'message': 'Email is already registered' if user else 'Email is available'
    })
