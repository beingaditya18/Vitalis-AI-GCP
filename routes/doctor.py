from flask import Blueprint, request, jsonify, render_template
from models import db, Consultation, Patient
from services.gemini_service import gemini_service

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'new_cases': 5,
        'total_assessments': 120,
        'high_risk_alerts': 2,
        'critical_risk': 1
    })

@doctor_bp.route('/patients/search', methods=['GET'])
def search_patients():
    query = request.args.get('q', '').lower()
    # Dummy Indian Patients
    patients = [
        {'id': 101, 'name': 'Rajesh Kumar', 'age': 45, 'gender': 'Male'},
        {'id': 102, 'name': 'Priya Sharma', 'age': 32, 'gender': 'Female'},
        {'id': 103, 'name': 'Amit Patel', 'age': 55, 'gender': 'Male'},
        {'id': 104, 'name': 'Sunita Singh', 'age': 28, 'gender': 'Female'},
        {'id': 105, 'name': 'Vikram Reddy', 'age': 60, 'gender': 'Male'}
    ]
    results = [p for p in patients if query in p['name'].lower() or query in str(p['id'])]
    return jsonify({'success': True, 'data': results})

@doctor_bp.route('/patients/queue/today', methods=['GET'])
def queue_today():
    # Return dummy Indian data instead of DB for demo impressiveness
    res = [
        {'id': 201, 'name': 'Anjali Desai', 'symptoms': 'Severe chest pain radiating to left arm, sweating, shortness of breath.', 'severity': 'High', 'status': 'pending', 'risk_score': 92},
        {'id': 202, 'name': 'Ramesh Iyer', 'symptoms': 'Persistent cough for 3 weeks, low-grade fever, night sweats.', 'severity': 'Medium', 'status': 'pending', 'risk_score': 65},
        {'id': 203, 'name': 'Kavita Menon', 'symptoms': 'Frequent urination, excessive thirst, blurred vision.', 'severity': 'Medium', 'status': 'pending', 'risk_score': 70}
    ]
    return jsonify({'success': True, 'data': {'queue': res}})

@doctor_bp.route('/patients/high-risk', methods=['GET'])
def high_risk():
    res = [
        {
            'prediction_id': '8842', 'disease': 'Acute Myocardial Infarction',
            'patient_age': 58, 'confidence_score': 0.94,
            'risk_level': 'critical', 'ml_probability': 0.94,
            'created_at': '2026-04-28T10:00:00Z'
        },
        {
            'prediction_id': '8843', 'disease': 'Diabetic Ketoacidosis',
            'patient_age': 42, 'confidence_score': 0.88,
            'risk_level': 'high', 'ml_probability': 0.88,
            'created_at': '2026-04-28T14:30:00Z'
        }
    ]
    return jsonify({'success': True, 'data': res})

@doctor_bp.route('/pending-summaries', methods=['GET'])
def pending_summaries():
    return jsonify({'pending': []})

@doctor_bp.route('/activity-feed', methods=['GET'])
def activity_feed():
    return jsonify({'activities': []})

@doctor_bp.route('/review/<int:case_id>', methods=['GET'])
def review_case(case_id):
    c = Consultation.query.get(case_id)
    if not c:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({
        'id': c.id,
        'symptoms': c.symptoms,
        'ai_summary': c.ai_summary
    })

@doctor_bp.route('/decision/<int:case_id>', methods=['POST'])
def make_decision(case_id):
    data = request.get_json()
    c = Consultation.query.get(case_id)
    if not c:
        return jsonify({'error': 'Not found'}), 404
    
    c.doctor_decision = data.get('decision')
    c.status = 'reviewed'
    db.session.commit()
    
    return jsonify({'message': 'Decision saved'})

@doctor_bp.route('/summary/generate', methods=['POST'])
def generate_summary():
    return jsonify({'message': 'Generated manually'})

@doctor_bp.route('/risk-assessment', methods=['POST'])
def risk_assessment():
    return jsonify({'score': 85})

@doctor_bp.route('/shap', methods=['GET'])
def get_shap():
    return jsonify({'explainability': 'Mock SHAP values'})

@doctor_bp.route('/rag-query', methods=['POST'])
def rag_query():
    return jsonify({'citations': ['Mock citation 1', 'Mock citation 2']})
