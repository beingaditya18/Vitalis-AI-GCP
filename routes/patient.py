from flask import Blueprint, request, jsonify
from models import db, Consultation, Patient, Appointment, AuditLog
from services.gemini_service import gemini_service
import os

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/consultation', methods=['POST'])
def create_consultation():
    data = request.get_json()
    patient_id = data.get('patient_id', 1) # Mock patient ID
    symptoms = data.get('symptoms')
    duration = data.get('duration')
    severity = data.get('severity')
    
    patient_text = f"Symptoms: {symptoms}. Duration: {duration}. Severity: {severity}."
    
    # Generate AI summary
    ai_summary = gemini_service.generate_clinical_summary(patient_text)
    safe_guidance = gemini_service.generate_patient_safe_message(ai_summary)
    
    consultation = Consultation(
        patient_id=patient_id,
        symptoms=symptoms,
        duration=duration,
        severity=severity,
        ai_summary=ai_summary,
        safe_guidance=safe_guidance
    )
    db.session.add(consultation)
    db.session.commit()
    
    return jsonify({
        'message': 'Consultation created',
        'consultation_id': consultation.id,
        'safe_guidance': safe_guidance
    })

@patient_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # In a real app, save securely
    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

@patient_bp.route('/appointments', methods=['GET'])
def get_appointments():
    return jsonify({'appointments': []})

@patient_bp.route('/appointments/upcoming', methods=['GET'])
def get_upcoming_appointments():
    return jsonify({'upcoming': []})

@patient_bp.route('/appointments/past', methods=['GET'])
def get_past_appointments():
    return jsonify({'past': []})

@patient_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    return jsonify({'message': 'Feedback received'})

@patient_bp.route('/reschedule', methods=['POST'])
def reschedule():
    return jsonify({'message': 'Appointment rescheduled'})

@patient_bp.route('/call-request', methods=['POST'])
def request_call():
    log = AuditLog(action='IVRS Call Requested', target_id=1) # Mock patient ID
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'Call requested successfully'})

@patient_bp.route('/emergency', methods=['POST'])
def emergency_alert():
    log = AuditLog(action='Emergency Alert', target_id=1) # Mock patient ID
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'Emergency request sent'})

@patient_bp.route('/insurance', methods=['GET'])
def get_insurance():
    return jsonify({'status': 'Active', 'provider': 'Demo Insurance'})
