from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    mobile = db.Column(db.String(15), unique=True, nullable=True)  # Primary identifier
    password_hash = db.Column(db.String(256), nullable=True)
    role = db.Column(db.String(20), nullable=False)  # patient, doctor, asha, admin, facility
    is_mobile_verified = db.Column(db.Boolean, default=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    patient_profile = db.relationship('Patient', backref='user', uselist=False)
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)
    asha_profile = db.relationship('ASHAWorker', backref='user', uselist=False)
    facility_profile = db.relationship('Facility', backref='user', uselist=False, foreign_keys='Facility.user_id')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'mobile': self.mobile,
            'role': self.role,
            'is_mobile_verified': self.is_mobile_verified,
            'is_email_verified': self.is_email_verified,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat()
        }

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100))
    mobile = db.Column(db.String(15))  # Duplicate for quick access
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    blood_group = db.Column(db.String(5))
    abha_number = db.Column(db.String(20))          # ABHA 14-digit number
    insurance_status = db.Column(db.String(50))
    emergency_contact = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    consultations = db.relationship('Consultation', backref='patient', lazy=True)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100))
    mobile = db.Column(db.String(15))  # Duplicate for quick access
    specialty = db.Column(db.String(100))
    license_number = db.Column(db.String(50))
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=True)
    is_available_today = db.Column(db.Boolean, default=True)

class ASHAWorker(db.Model):
    __tablename__ = 'asha_workers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100))
    assigned_villages = db.Column(db.String(255))
    total_patients = db.Column(db.Integer, default=0)
    tasks_completed = db.Column(db.Integer, default=0)

class Facility(db.Model):
    __tablename__ = 'facilities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # linked login
    name = db.Column(db.String(150), nullable=False)
    license_number = db.Column(db.String(100))
    specialties = db.Column(db.String(255))
    address = db.Column(db.Text)
    pin_code = db.Column(db.String(10))
    district = db.Column(db.String(80))
    block = db.Column(db.String(80))
    village = db.Column(db.String(80))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    photo_url = db.Column(db.String(255))           # geotagged photo path
    poc_name = db.Column(db.String(100))            # Point of Contact
    poc_mobile = db.Column(db.String(20))
    login_id = db.Column(db.String(50), unique=True, nullable=True)  # auto-generated
    is_active = db.Column(db.Boolean, default=True)
    otp_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctors = db.relationship('FacilityDoctor', backref='facility', lazy=True)
    services = db.relationship('DiagnosticService', backref='facility', lazy=True)
    slots = db.relationship('AppointmentSlot', backref='facility', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'license_number': self.license_number,
            'specialties': self.specialties,
            'address': self.address,
            'pin_code': self.pin_code,
            'district': self.district,
            'block': self.block,
            'village': self.village,
            'lat': self.lat,
            'lng': self.lng,
            'photo_url': self.photo_url,
            'poc_name': self.poc_name,
            'poc_mobile': self.poc_mobile,
            'login_id': self.login_id,
            'is_active': self.is_active,
            'otp_verified': self.otp_verified,
            'created_at': self.created_at.isoformat()
        }

class FacilityDoctor(db.Model):
    __tablename__ = 'facility_doctors'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    qualification = db.Column(db.String(150))
    schedule = db.Column(db.String(255))             # e.g. "Mon-Fri 9AM-5PM"
    is_available_today = db.Column(db.Boolean, default=True)
    consultation_fee = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'facility_id': self.facility_id,
            'name': self.name,
            'specialty': self.specialty,
            'qualification': self.qualification,
            'schedule': self.schedule,
            'is_available_today': self.is_available_today,
            'consultation_fee': self.consultation_fee
        }

class DiagnosticService(db.Model):
    __tablename__ = 'diagnostic_services'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=False)
    service_name = db.Column(db.String(150), nullable=False)
    service_type = db.Column(db.String(50))          # OPD / Diagnostic / Lab
    price = db.Column(db.Float, default=0.0)
    is_available_today = db.Column(db.Boolean, default=True)
    turnaround_hours = db.Column(db.Integer, default=24)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'facility_id': self.facility_id,
            'service_name': self.service_name,
            'service_type': self.service_type,
            'price': self.price,
            'is_available_today': self.is_available_today,
            'turnaround_hours': self.turnaround_hours
        }

class AppointmentSlot(db.Model):
    __tablename__ = 'appointment_slots'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=False)
    facility_doctor_id = db.Column(db.Integer, db.ForeignKey('facility_doctors.id'), nullable=True)
    slot_date = db.Column(db.Date, nullable=False)
    slot_time = db.Column(db.String(10), nullable=False)   # "10:00"
    is_booked = db.Column(db.Boolean, default=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'facility_id': self.facility_id,
            'facility_doctor_id': self.facility_doctor_id,
            'slot_date': self.slot_date.isoformat() if self.slot_date else None,
            'slot_time': self.slot_time,
            'is_booked': self.is_booked
        }

class Consultation(db.Model):
    __tablename__ = 'consultations'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50))
    severity = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')  # pending, reviewed
    ai_summary = db.Column(db.Text)
    safe_guidance = db.Column(db.Text)
    risk_score = db.Column(db.Integer, default=0)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)
    doctor_decision = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    files = db.relationship('File', backref='consultation', lazy=True)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=True)
    facility_doctor_id = db.Column(db.Integer, db.ForeignKey('facility_doctors.id'), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, rescheduled
    type = db.Column(db.String(50))   # OPD / Diagnostic / Consultation
    service_name = db.Column(db.String(150))
    notes = db.Column(db.Text)
    is_visited = db.Column(db.Boolean, default=False)
    sms_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'facility_id': self.facility_id,
            'date': self.date.isoformat(),
            'status': self.status,
            'type': self.type,
            'service_name': self.service_name,
            'notes': self.notes,
            'is_visited': self.is_visited,
            'sms_sent': self.sms_sent
        }

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultations.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))  # image, video, pdf
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    rating = db.Column(db.Integer)  # 1-5
    comments = db.Column(db.Text)
    visit_status = db.Column(db.String(20), default='visited')   # visited / not_visited
    callback_status = db.Column(db.String(20), default='pending')  # pending, called, resolved
    reschedule_date = db.Column(db.DateTime, nullable=True)
    reschedule_sms_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'rating': self.rating,
            'comments': self.comments,
            'visit_status': self.visit_status,
            'callback_status': self.callback_status,
            'reschedule_date': self.reschedule_date.isoformat() if self.reschedule_date else None
        }

class CRMCase(db.Model):
    __tablename__ = 'crm_cases'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    district = db.Column(db.String(50))
    block = db.Column(db.String(50))
    village = db.Column(db.String(50))
    health_issue = db.Column(db.Text)
    abha_number = db.Column(db.String(20))
    recommended_facilities = db.Column(db.Text)  # JSON string of facility IDs/names
    status = db.Column(db.String(20), default='open')   # open, booked, visited, closed
    assigned_facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    sms_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_name': self.patient_name,
            'phone': self.phone,
            'district': self.district,
            'block': self.block,
            'village': self.village,
            'health_issue': self.health_issue,
            'abha_number': self.abha_number,
            'status': self.status,
            'assigned_facility_id': self.assigned_facility_id,
            'sms_sent': self.sms_sent,
            'created_at': self.created_at.isoformat()
        }

class ASHATask(db.Model):
    __tablename__ = 'asha_tasks'
    id = db.Column(db.Integer, primary_key=True)
    asha_id = db.Column(db.Integer, db.ForeignKey('asha_workers.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)
    description = db.Column(db.String(255), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100))
    target_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class OTPVerification(db.Model):
    __tablename__ = 'otp_verifications'
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(15), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    purpose = db.Column(db.String(20), nullable=False)  # login, registration, password_reset
    is_verified = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        return {
            'id': self.id,
            'mobile': self.mobile,
            'purpose': self.purpose,
            'is_verified': self.is_verified,
            'expires_at': self.expires_at.isoformat(),
            'created_at': self.created_at.isoformat()
        }
