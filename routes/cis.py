from flask import Blueprint, jsonify, request, session
from models import db, Facility, CRMCase, User, Appointment
from services.mock_abha import generate_mock_abha, generate_facility_login_id, generate_temp_password
from services.mock_notifications import generate_otp_mock, verify_otp_mock, send_credentials_sms
from werkzeug.security import generate_password_hash

cis_bp = Blueprint('cis', __name__)

# ──────────────────────────────────────────────
# FACILITY REGISTRATION & OTP
# ──────────────────────────────────────────────

@cis_bp.route('/facility/register/otp/send', methods=['POST'])
def send_registration_otp():
    data = request.get_json()
    phone = data.get('poc_mobile')
    if not phone:
        return jsonify({'error': 'Mobile number required'}), 400
    otp = generate_otp_mock(phone)
    return jsonify({'message': 'OTP sent successfully', 'mock_otp_for_testing': otp})

@cis_bp.route('/facility/register', methods=['POST'])
def register_facility():
    data = request.get_json()
    phone = data.get('poc_mobile')
    otp = data.get('otp')
    
    if not verify_otp_mock(phone, otp):
        return jsonify({'error': 'Invalid or expired OTP'}), 400

    # Create Facility User
    login_id = generate_facility_login_id(data.get('name'))
    temp_pass = generate_temp_password()
    
    user = User(
        email=f"{login_id.lower()}@facility.vitalis.com",
        password_hash=generate_password_hash(temp_pass),
        role='facility'
    )
    db.session.add(user)
    db.session.flush()

    f = Facility(
        user_id=user.id,
        name=data.get('name'),
        license_number=data.get('license_number'),
        specialties=data.get('specialties'),
        address=data.get('address'),
        pin_code=data.get('pin_code'),
        district=data.get('district'),
        block=data.get('block'),
        village=data.get('village'),
        lat=data.get('lat'),
        lng=data.get('lng'),
        photo_url=data.get('photo_url'),
        poc_name=data.get('poc_name'),
        poc_mobile=phone,
        login_id=login_id,
        otp_verified=True
    )
    db.session.add(f)
    db.session.commit()

    # Send credentials via SMS
    send_credentials_sms(phone, f.name, login_id, temp_pass)

    return jsonify({
        'message': 'Facility registered successfully', 
        'id': f.id,
        'login_id': login_id
    })

@cis_bp.route('/facility/list', methods=['GET'])
def list_facilities():
    facilities = Facility.query.filter_by(is_active=True).all()
    res = [f.to_dict() for f in facilities]
    return jsonify({'facilities': res})

# ──────────────────────────────────────────────
# CALL CENTER CRM
# ──────────────────────────────────────────────

@cis_bp.route('/call-center/lead', methods=['POST'])
def call_center_lead():
    data = request.get_json()
    case = CRMCase(
        patient_name=data.get('patient_name'),
        phone=data.get('phone'),
        district=data.get('district'),
        block=data.get('block'),
        village=data.get('village'),
        health_issue=data.get('health_issue')
    )
    db.session.add(case)
    db.session.commit()
    
    # Mock AI Facility Recommendation based on district/issue
    recommended = [
        {'id': 1, 'name': 'City General Hospital', 'distance': '2.5 km', 'rating': 4.8, 'specialties': 'General, Orthopaedics'},
        {'id': 2, 'name': 'Sunrise Care Clinic', 'distance': '5.1 km', 'rating': 4.5, 'specialties': 'General, Pediatrics'},
        {'id': 3, 'name': 'Metro Health Centre', 'distance': '8.0 km', 'rating': 4.2, 'specialties': 'Cardiology, General'}
    ]
    import json
    case.recommended_facilities = json.dumps(recommended)
    db.session.commit()
    
    return jsonify({
        'message': 'Lead registered', 
        'case_id': case.id,
        'recommendations': recommended
    })

@cis_bp.route('/call-center/webhook', methods=['POST'])
def call_center_webhook():
    # Placeholder for Twilio/Exotel IVRS webhook
    return jsonify({'message': 'Webhook processed'})

@cis_bp.route('/appointment/book', methods=['POST'])
def book_appointment():
    # Used by CRM to book on behalf of patient
    data = request.get_json()
    from datetime import datetime
    appt = Appointment(
        patient_id=data.get('patient_id', 1),
        facility_id=data.get('facility_id'),
        date=datetime.fromisoformat(data.get('date')),
        type=data.get('type', 'OPD'),
        notes=data.get('notes', '')
    )
    db.session.add(appt)
    
    if data.get('case_id'):
        case = CRMCase.query.get(data['case_id'])
        if case:
            case.status = 'booked'
            case.appointment_id = appt.id
            case.assigned_facility_id = data.get('facility_id')
            
    db.session.commit()
    
    # Mock SMS
    from services.mock_notifications import send_appointment_sms
    facility = Facility.query.get(data.get('facility_id'))
    fac_name = facility.name if facility else "Hospital"
    
    sms_res = send_appointment_sms(
        phone=data.get('phone', '9000000000'),
        patient_name=data.get('patient_name', 'Patient'),
        facility_name=fac_name,
        appointment_date=appt.date.strftime('%d %b %Y %I:%M %p'),
        appointment_id=appt.id
    )
    
    return jsonify({'message': 'Appointment booked', 'sms_status': sms_res['status']})

# ──────────────────────────────────────────────
# REPORTS & ABHA
# ──────────────────────────────────────────────

@cis_bp.route('/appointment/reports/daily', methods=['GET'])
def daily_reports():
    return jsonify({'report': 'Mock Daily Report'})

@cis_bp.route('/abha/generate', methods=['POST'])
def abha_generate():
    data = request.get_json()
    mock_abha = generate_mock_abha(
        name=data.get('name', 'Patient'),
        dob=data.get('dob', '1990-01-01'),
        gender=data.get('gender', 'M'),
        phone=data.get('phone', '9000000000')
    )
    
    # Attach to case if case_id provided
    if data.get('case_id'):
        case = CRMCase.query.get(data['case_id'])
        if case:
            case.abha_number = mock_abha['abha_number']
            db.session.commit()
            
    return jsonify({'success': True, 'abha_data': mock_abha})
