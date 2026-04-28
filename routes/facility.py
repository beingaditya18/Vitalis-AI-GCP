from flask import Blueprint, jsonify, request
from models import (db, Facility, FacilityDoctor, DiagnosticService,
                    AppointmentSlot, Appointment, AuditLog)
from services.mock_notifications import send_credentials_sms, generate_otp_mock, verify_otp_mock
from services.mock_abha import generate_facility_login_id, generate_temp_password
from datetime import datetime, date
import json

facility_bp = Blueprint('facility', __name__)

# ──────────────────────────────────────────────
# FACILITY PROFILE
# ──────────────────────────────────────────────

@facility_bp.route('/profile', methods=['GET'])
def get_profile():
    facility_id = request.args.get('id', 1)
    f = Facility.query.get(facility_id)
    if not f:
        return jsonify({'error': 'Facility not found'}), 404
    doctors = [d.to_dict() for d in FacilityDoctor.query.filter_by(facility_id=f.id).all()]
    services = [s.to_dict() for s in DiagnosticService.query.filter_by(facility_id=f.id).all()]
    result = f.to_dict()
    result['doctors'] = doctors
    result['services'] = services
    return jsonify({'facility': result})

@facility_bp.route('/profile', methods=['PUT'])
def update_profile():
    data = request.get_json()
    facility_id = data.get('id', 1)
    f = Facility.query.get(facility_id)
    if not f:
        return jsonify({'error': 'Facility not found'}), 404
    for field in ['name', 'address', 'pin_code', 'district', 'block',
                  'village', 'specialties', 'poc_name', 'poc_mobile', 'lat', 'lng']:
        if field in data:
            setattr(f, field, data[field])
    db.session.commit()
    log = AuditLog(action='FACILITY_PROFILE_UPDATED', target_id=f.id,
                   details=f"Updated by POC: {f.poc_name}")
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'Profile updated', 'facility': f.to_dict()})

# ──────────────────────────────────────────────
# DOCTOR MANAGEMENT
# ──────────────────────────────────────────────

@facility_bp.route('/doctors', methods=['GET'])
def get_doctors():
    facility_id = request.args.get('facility_id', 1)
    doctors = FacilityDoctor.query.filter_by(facility_id=facility_id).all()
    return jsonify({'doctors': [d.to_dict() for d in doctors]})

@facility_bp.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.get_json()
    doc = FacilityDoctor(
        facility_id=data.get('facility_id', 1),
        name=data.get('name'),
        specialty=data.get('specialty'),
        qualification=data.get('qualification'),
        schedule=data.get('schedule'),
        consultation_fee=data.get('consultation_fee', 0.0),
        is_available_today=data.get('is_available_today', True)
    )
    db.session.add(doc)
    db.session.commit()
    return jsonify({'message': 'Doctor added', 'doctor': doc.to_dict()}), 201

@facility_bp.route('/doctors/<int:doc_id>', methods=['PUT'])
def update_doctor(doc_id):
    data = request.get_json()
    doc = FacilityDoctor.query.get(doc_id)
    if not doc:
        return jsonify({'error': 'Doctor not found'}), 404
    for field in ['name', 'specialty', 'qualification', 'schedule',
                  'consultation_fee', 'is_available_today']:
        if field in data:
            setattr(doc, field, data[field])
    db.session.commit()
    return jsonify({'message': 'Doctor updated', 'doctor': doc.to_dict()})

@facility_bp.route('/doctors/<int:doc_id>', methods=['DELETE'])
def delete_doctor(doc_id):
    doc = FacilityDoctor.query.get(doc_id)
    if not doc:
        return jsonify({'error': 'Doctor not found'}), 404
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'message': 'Doctor removed'})

@facility_bp.route('/doctors/<int:doc_id>/availability', methods=['POST'])
def toggle_doctor_availability(doc_id):
    data = request.get_json()
    doc = FacilityDoctor.query.get(doc_id)
    if not doc:
        return jsonify({'error': 'Doctor not found'}), 404
    doc.is_available_today = data.get('is_available', not doc.is_available_today)
    db.session.commit()
    return jsonify({'message': 'Availability updated', 'is_available_today': doc.is_available_today})

# ──────────────────────────────────────────────
# DIAGNOSTIC SERVICES
# ──────────────────────────────────────────────

@facility_bp.route('/services', methods=['GET'])
def get_services():
    facility_id = request.args.get('facility_id', 1)
    services = DiagnosticService.query.filter_by(facility_id=facility_id).all()
    return jsonify({'services': [s.to_dict() for s in services]})

@facility_bp.route('/services', methods=['POST'])
def add_service():
    data = request.get_json()
    svc = DiagnosticService(
        facility_id=data.get('facility_id', 1),
        service_name=data.get('service_name'),
        service_type=data.get('service_type', 'OPD'),
        price=data.get('price', 0.0),
        is_available_today=data.get('is_available_today', True),
        turnaround_hours=data.get('turnaround_hours', 24)
    )
    db.session.add(svc)
    db.session.commit()
    return jsonify({'message': 'Service added', 'service': svc.to_dict()}), 201

@facility_bp.route('/services/<int:svc_id>/availability', methods=['POST'])
def toggle_service_availability(svc_id):
    data = request.get_json()
    svc = DiagnosticService.query.get(svc_id)
    if not svc:
        return jsonify({'error': 'Service not found'}), 404
    svc.is_available_today = data.get('is_available', not svc.is_available_today)
    db.session.commit()
    return jsonify({'message': 'Service availability updated', 'is_available_today': svc.is_available_today})

@facility_bp.route('/services/<int:svc_id>', methods=['DELETE'])
def delete_service(svc_id):
    svc = DiagnosticService.query.get(svc_id)
    if not svc:
        return jsonify({'error': 'Service not found'}), 404
    db.session.delete(svc)
    db.session.commit()
    return jsonify({'message': 'Service removed'})

# ──────────────────────────────────────────────
# APPOINTMENT SLOTS
# ──────────────────────────────────────────────

@facility_bp.route('/slots', methods=['GET'])
def get_slots():
    facility_id = request.args.get('facility_id', 1)
    slot_date_str = request.args.get('date', date.today().isoformat())
    try:
        slot_date = date.fromisoformat(slot_date_str)
    except ValueError:
        slot_date = date.today()
    slots = AppointmentSlot.query.filter_by(
        facility_id=facility_id, slot_date=slot_date
    ).all()
    return jsonify({'slots': [s.to_dict() for s in slots]})

@facility_bp.route('/slots', methods=['POST'])
def add_slot():
    data = request.get_json()
    slot_date = date.fromisoformat(data.get('slot_date', date.today().isoformat()))
    slot = AppointmentSlot(
        facility_id=data.get('facility_id', 1),
        facility_doctor_id=data.get('facility_doctor_id'),
        slot_date=slot_date,
        slot_time=data.get('slot_time', '09:00')
    )
    db.session.add(slot)
    db.session.commit()
    return jsonify({'message': 'Slot added', 'slot': slot.to_dict()}), 201

# ──────────────────────────────────────────────
# APPOINTMENTS (Facility View)
# ──────────────────────────────────────────────

@facility_bp.route('/appointments', methods=['GET'])
def get_appointments():
    facility_id = request.args.get('facility_id', 1)
    date_str = request.args.get('date')
    doctor_id = request.args.get('doctor_id')

    query = Appointment.query.filter_by(facility_id=facility_id)
    if date_str:
        try:
            filter_date = datetime.fromisoformat(date_str).date()
            query = query.filter(db.func.date(Appointment.date) == filter_date)
        except ValueError:
            pass
    if doctor_id:
        query = query.filter_by(facility_doctor_id=doctor_id)

    appointments = query.order_by(Appointment.date.desc()).all()
    return jsonify({'appointments': [a.to_dict() for a in appointments]})

@facility_bp.route('/appointments/book', methods=['POST'])
def book_appointment():
    data = request.get_json()
    appt = Appointment(
        patient_id=data.get('patient_id', 1),
        facility_id=data.get('facility_id', 1),
        facility_doctor_id=data.get('facility_doctor_id'),
        date=datetime.fromisoformat(data.get('date')),
        type=data.get('type', 'OPD'),
        service_name=data.get('service_name'),
        notes=data.get('notes', '')
    )
    db.session.add(appt)
    db.session.commit()

    # Mark slot as booked
    if data.get('slot_id'):
        slot = AppointmentSlot.query.get(data['slot_id'])
        if slot:
            slot.is_booked = True
            slot.appointment_id = appt.id
            db.session.commit()

    # Mock SMS notification
    from services.mock_notifications import send_appointment_sms
    sms_result = send_appointment_sms(
        phone=data.get('patient_phone', '9000000000'),
        patient_name=data.get('patient_name', 'Patient'),
        facility_name=data.get('facility_name', 'Facility'),
        appointment_date=appt.date.strftime('%d %b %Y %I:%M %p'),
        appointment_id=appt.id
    )
    appt.sms_sent = sms_result.get('success', False)
    db.session.commit()

    log = AuditLog(action='APPOINTMENT_BOOKED', target_id=appt.id,
                   details=f"Facility: {data.get('facility_id')}, SMS: {appt.sms_sent}")
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'message': 'Appointment booked',
        'appointment': appt.to_dict(),
        'sms_sent': appt.sms_sent
    }), 201

@facility_bp.route('/appointments/report', methods=['GET'])
def download_report():
    facility_id = request.args.get('facility_id', 1)
    date_str = request.args.get('date', date.today().isoformat())
    doctor_id = request.args.get('doctor_id')

    # Mock report data for demo
    mock_report = {
        'facility_id': facility_id,
        'report_date': date_str,
        'generated_at': datetime.utcnow().isoformat(),
        'total_appointments': 12,
        'visited': 9,
        'not_visited': 3,
        'by_doctor': [
            {'doctor': 'Dr. Rakesh Sharma', 'specialty': 'General Medicine',
             'appointments': 5, 'visited': 4, 'not_visited': 1},
            {'doctor': 'Dr. Sunita Patel', 'specialty': 'Gynaecology',
             'appointments': 4, 'visited': 3, 'not_visited': 1},
            {'doctor': 'Dr. Amit Kumar', 'specialty': 'Orthopaedics',
             'appointments': 3, 'visited': 2, 'not_visited': 1},
        ],
        'appointments': [
            {'id': 1001, 'patient': 'Radha Sharma', 'time': '09:00', 'type': 'OPD',
             'doctor': 'Dr. Rakesh Sharma', 'status': 'visited'},
            {'id': 1002, 'patient': 'Suresh Kumar', 'time': '09:30', 'type': 'Diagnostic',
             'doctor': 'Dr. Sunita Patel', 'status': 'visited'},
            {'id': 1003, 'patient': 'Meena Devi', 'time': '10:00', 'type': 'OPD',
             'doctor': 'Dr. Amit Kumar', 'status': 'not_visited'},
        ]
    }
    return jsonify({'report': mock_report})
