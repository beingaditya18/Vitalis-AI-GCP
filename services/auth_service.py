from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, OTPVerification, Patient, Doctor, ASHAWorker, Facility, AuditLog
from datetime import datetime, timedelta
import random
import re

class AuthService:
    """Comprehensive authentication service with mobile OTP support"""
    
    OTP_EXPIRY_MINUTES = 10
    MAX_OTP_ATTEMPTS = 3
    
    @staticmethod
    def validate_mobile(mobile):
        """Validate Indian mobile number format"""
        pattern = r'^[6-9]\d{9}$'
        return bool(re.match(pattern, mobile))
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def generate_otp():
        """Generate 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def send_otp(mobile, purpose='login'):
        """
        Generate and send OTP to mobile number
        Purpose: login, registration, password_reset
        """
        if not AuthService.validate_mobile(mobile):
            return {'success': False, 'error': 'Invalid mobile number format'}
        
        # Invalidate previous OTPs for this mobile and purpose
        OTPVerification.query.filter_by(
            mobile=mobile, 
            purpose=purpose, 
            is_verified=False
        ).update({'is_verified': True})  # Mark as used
        
        # Generate new OTP
        otp_code = AuthService.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=AuthService.OTP_EXPIRY_MINUTES)
        
        otp_record = OTPVerification(
            mobile=mobile,
            otp_code=otp_code,
            purpose=purpose,
            expires_at=expires_at
        )
        db.session.add(otp_record)
        db.session.commit()
        
        # Mock SMS sending (replace with actual SMS gateway)
        from services.mock_notifications import send_otp_sms
        sms_result = send_otp_sms(mobile, otp_code)
        
        return {
            'success': True,
            'message': f'OTP sent to {mobile}',
            'otp_id': otp_record.id,
            'expires_in_minutes': AuthService.OTP_EXPIRY_MINUTES,
            'mock_otp': otp_code  # Remove in production
        }
    
    @staticmethod
    def verify_otp(mobile, otp_code, purpose='login'):
        """Verify OTP code"""
        otp_record = OTPVerification.query.filter_by(
            mobile=mobile,
            purpose=purpose,
            is_verified=False
        ).order_by(OTPVerification.created_at.desc()).first()
        
        if not otp_record:
            return {'success': False, 'error': 'No OTP found for this mobile number'}
        
        if otp_record.is_expired():
            return {'success': False, 'error': 'OTP has expired'}
        
        if otp_record.attempts >= AuthService.MAX_OTP_ATTEMPTS:
            return {'success': False, 'error': 'Maximum OTP attempts exceeded'}
        
        # Increment attempts
        otp_record.attempts += 1
        db.session.commit()
        
        if otp_record.otp_code != otp_code:
            return {
                'success': False, 
                'error': 'Invalid OTP',
                'attempts_remaining': AuthService.MAX_OTP_ATTEMPTS - otp_record.attempts
            }
        
        # Mark as verified
        otp_record.is_verified = True
        db.session.commit()
        
        return {'success': True, 'message': 'OTP verified successfully'}
    
    @staticmethod
    def register_user(mobile, role, name=None, email=None, password=None, **profile_data):
        """
        Register new user with mobile number
        Supports: patient, doctor, asha, admin, facility
        """
        if not AuthService.validate_mobile(mobile):
            return {'success': False, 'error': 'Invalid mobile number'}
        
        # Check if user already exists
        existing_user = User.query.filter_by(mobile=mobile).first()
        if existing_user:
            return {'success': False, 'error': 'Mobile number already registered'}
        
        if email and not AuthService.validate_email(email):
            return {'success': False, 'error': 'Invalid email format'}
        
        # Create user
        user = User(
            mobile=mobile,
            email=email,
            role=role,
            is_mobile_verified=True,  # Assumed verified via OTP
            password_hash=generate_password_hash(password) if password else None
        )
        db.session.add(user)
        db.session.flush()  # Get user.id
        
        # Create role-specific profile
        profile = None
        if role == 'patient':
            profile = Patient(
                user_id=user.id,
                name=name or profile_data.get('name'),
                mobile=mobile,
                age=profile_data.get('age'),
                gender=profile_data.get('gender'),
                blood_group=profile_data.get('blood_group'),
                abha_number=profile_data.get('abha_number'),
                emergency_contact=profile_data.get('emergency_contact')
            )
        elif role == 'doctor':
            profile = Doctor(
                user_id=user.id,
                name=name or profile_data.get('name'),
                mobile=mobile,
                specialty=profile_data.get('specialty'),
                license_number=profile_data.get('license_number'),
                facility_id=profile_data.get('facility_id')
            )
        elif role == 'asha':
            profile = ASHAWorker(
                user_id=user.id,
                name=name or profile_data.get('name'),
                assigned_villages=profile_data.get('assigned_villages')
            )
        elif role == 'facility':
            # For facility, create new facility record
            facility = Facility(
                user_id=user.id,
                name=name or profile_data.get('name'),
                poc_name=name or profile_data.get('name'),
                poc_mobile=mobile,
                license_number=profile_data.get('license_number'),
                address=profile_data.get('address'),
                district=profile_data.get('district'),
                block=profile_data.get('block'),
                village=profile_data.get('village'),
                pin_code=profile_data.get('pin_code'),
                specialties=profile_data.get('specialties'),
                otp_verified=True,
                is_active=True
            )
            profile = facility
        
        if profile:
            db.session.add(profile)
        
        db.session.commit()
        
        # Log registration
        log = AuditLog(
            user_id=user.id,
            action='USER_REGISTERED',
            details=f'Role: {role}, Mobile: {mobile}'
        )
        db.session.add(log)
        db.session.commit()
        
        return {
            'success': True,
            'message': 'User registered successfully',
            'user': user.to_dict()
        }
    
    @staticmethod
    def login_with_mobile(mobile, otp_code=None, password=None):
        """
        Login with mobile number using OTP or password
        """
        if not AuthService.validate_mobile(mobile):
            return {'success': False, 'error': 'Invalid mobile number'}
        
        user = User.query.filter_by(mobile=mobile).first()
        
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        if not user.is_active:
            return {'success': False, 'error': 'Account is deactivated'}
        
        # Verify OTP if provided
        if otp_code:
            otp_result = AuthService.verify_otp(mobile, otp_code, 'login')
            if not otp_result['success']:
                return otp_result
        # Verify password if provided
        elif password:
            if not user.password_hash:
                return {'success': False, 'error': 'Password not set for this account'}
            if not check_password_hash(user.password_hash, password):
                return {'success': False, 'error': 'Invalid password'}
        else:
            return {'success': False, 'error': 'OTP or password required'}
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Log login
        log = AuditLog(
            user_id=user.id,
            action='USER_LOGIN',
            details=f'Mobile: {mobile}'
        )
        db.session.add(log)
        db.session.commit()
        
        return {
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict()
        }
    
    @staticmethod
    def login_with_email(email, password):
        """Login with email and password"""
        if not AuthService.validate_email(email):
            return {'success': False, 'error': 'Invalid email format'}
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        if not user.is_active:
            return {'success': False, 'error': 'Account is deactivated'}
        
        if not user.password_hash:
            return {'success': False, 'error': 'Password not set for this account'}
        
        if not check_password_hash(user.password_hash, password):
            return {'success': False, 'error': 'Invalid password'}
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Log login
        log = AuditLog(
            user_id=user.id,
            action='USER_LOGIN',
            details=f'Email: {email}'
        )
        db.session.add(log)
        db.session.commit()
        
        return {
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict()
        }
    
    @staticmethod
    def reset_password(mobile, otp_code, new_password):
        """Reset password using OTP verification"""
        # Verify OTP
        otp_result = AuthService.verify_otp(mobile, otp_code, 'password_reset')
        if not otp_result['success']:
            return otp_result
        
        user = User.query.filter_by(mobile=mobile).first()
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        # Update password
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        # Log password reset
        log = AuditLog(
            user_id=user.id,
            action='PASSWORD_RESET',
            details=f'Mobile: {mobile}'
        )
        db.session.add(log)
        db.session.commit()
        
        return {'success': True, 'message': 'Password reset successfully'}
    
    @staticmethod
    def get_user_profile(user_id):
        """Get complete user profile with role-specific data"""
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        profile_data = user.to_dict()
        
        # Add role-specific profile
        if user.role == 'patient' and user.patient_profile:
            profile_data['profile'] = {
                'name': user.patient_profile.name,
                'mobile': user.patient_profile.mobile,
                'age': user.patient_profile.age,
                'gender': user.patient_profile.gender,
                'blood_group': user.patient_profile.blood_group,
                'abha_number': user.patient_profile.abha_number,
                'emergency_contact': user.patient_profile.emergency_contact
            }
        elif user.role == 'doctor' and user.doctor_profile:
            profile_data['profile'] = {
                'name': user.doctor_profile.name,
                'mobile': user.doctor_profile.mobile,
                'specialty': user.doctor_profile.specialty,
                'license_number': user.doctor_profile.license_number,
                'facility_id': user.doctor_profile.facility_id
            }
        elif user.role == 'asha' and user.asha_profile:
            profile_data['profile'] = {
                'name': user.asha_profile.name,
                'assigned_villages': user.asha_profile.assigned_villages,
                'total_patients': user.asha_profile.total_patients
            }
        elif user.role == 'facility' and user.facility_profile:
            profile_data['profile'] = user.facility_profile.to_dict()
        
        return {'success': True, 'user': profile_data}
