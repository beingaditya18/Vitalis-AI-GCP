from flask import Blueprint, jsonify, request
from models import db, AuditLog, Facility, Appointment, Feedback, CRMCase, Patient, Consultation
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/metrics', methods=['GET'])
def get_metrics():
    # Enhanced mock data with realistic numbers
    total_patients = Patient.query.count() or 1250
    active_facilities = Facility.query.filter_by(is_active=True).count() or 15
    total_appointments = Appointment.query.count() or 2450
    visited_appointments = Appointment.query.filter_by(is_visited=True).count() or 2080
    non_visited_appointments = total_appointments - visited_appointments
    total_feedback = Feedback.query.count() or 1850
    
    # AI usage stats
    total_consultations = Consultation.query.count() or 980
    ai_processed = Consultation.query.filter(Consultation.ai_summary.isnot(None)).count() or 856
    
    return jsonify({
        'total_patients': total_patients,
        'total_doctors': 68,
        'total_asha_workers': 45,
        'active_facilities': active_facilities,
        'total_appointments': total_appointments,
        'visited_appointments': visited_appointments,
        'non_visited_appointments': non_visited_appointments,
        'total_feedback': total_feedback,
        'ai_consultations': total_consultations,
        'ai_processed': ai_processed,
        'ai_usage_percent': round((ai_processed / total_consultations * 100) if total_consultations > 0 else 87.3, 1),
        'avg_rating': 4.2,
        'system_uptime': '99.8%'
    })

@admin_bp.route('/stats/drilldown', methods=['GET'])
def get_drilldown_stats():
    level = request.args.get('level', 'district') # district, block, village
    
    # Query real data from facilities and appointments
    if level == 'district':
        results = db.session.query(
            Facility.district,
            func.count(Appointment.id).label('count')
        ).join(Appointment, Appointment.facility_id == Facility.id, isouter=True)\
         .filter(Facility.district.isnot(None))\
         .group_by(Facility.district).all()
        
        data = {r.district: r.count for r in results} if results else {'Pune': 450, 'Mumbai': 600, 'Nagpur': 200}
        
    elif level == 'block':
        results = db.session.query(
            Facility.block,
            func.count(Appointment.id).label('count')
        ).join(Appointment, Appointment.facility_id == Facility.id, isouter=True)\
         .filter(Facility.block.isnot(None))\
         .group_by(Facility.block).all()
        
        data = {r.block: r.count for r in results} if results else {'Haveli': 150, 'Shirur': 100, 'Baramati': 200}
        
    else:  # village
        results = db.session.query(
            Facility.village,
            func.count(Appointment.id).label('count')
        ).join(Appointment, Appointment.facility_id == Facility.id, isouter=True)\
         .filter(Facility.village.isnot(None))\
         .group_by(Facility.village).all()
        
        data = {r.village: r.count for r in results} if results else {'Wagholi': 50, 'Loni': 40, 'Uruli': 60}
        
    return jsonify({
        'level': level,
        'labels': list(data.keys()),
        'values': list(data.values())
    })

@admin_bp.route('/facilities/full', methods=['GET'])
def get_facilities_full():
    facilities = Facility.query.all()
    res = []
    for f in facilities:
        d = f.to_dict()
        # Mocking doctor and appointment counts for admin view
        d['doctor_count'] = len(f.doctors) if hasattr(f, 'doctors') else 0
        d['appointment_count'] = 45 # Mock value
        res.append(d)
    return jsonify({'facilities': res})

@admin_bp.route('/crm/cases', methods=['GET'])
def get_crm_cases():
    cases = CRMCase.query.order_by(CRMCase.created_at.desc()).all()
    return jsonify({'cases': [c.to_dict() for c in cases]})

@admin_bp.route('/feedback', methods=['GET'])
def get_feedback():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    # Mock data if empty
    if not feedbacks:
        return jsonify({'feedback': [
            {'id': 1, 'patient_name': 'Ramesh Kumar', 'rating': 4, 'comments': 'Good service', 'visit_status': 'visited', 'callback_status': 'pending'},
            {'id': 2, 'patient_name': 'Sunita Devi', 'rating': 2, 'comments': 'Wait time was too long', 'visit_status': 'visited', 'callback_status': 'pending'},
            {'id': 3, 'patient_name': 'Amit Patel', 'rating': 0, 'comments': '', 'visit_status': 'not_visited', 'callback_status': 'pending'}
        ]})
    return jsonify({'feedback': [f.to_dict() for f in feedbacks]})

@admin_bp.route('/feedback/<int:f_id>/reschedule', methods=['POST'])
def reschedule_appointment(f_id):
    data = request.get_json()
    # Mock reschedule logic
    from services.mock_notifications import send_reschedule_sms
    send_reschedule_sms('9000000000', 'Patient', 'Hospital', data.get('new_date'), 1001)
    return jsonify({'message': 'Appointment rescheduled and SMS sent'})

@admin_bp.route('/chart-data', methods=['GET'])
def chart_data():
    # Appointments timeline (last 7 days) - Enhanced mock data
    today = datetime.now().date()
    timeline_data = []
    timeline_labels = []
    
    # Mock data with realistic patterns (weekdays higher than weekends)
    mock_pattern = [45, 52, 48, 38, 42, 28, 25]  # Mon-Sun pattern
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = Appointment.query.filter(
            func.date(Appointment.date) == date
        ).count()
        timeline_data.append(count if count > 0 else mock_pattern[6-i])
        timeline_labels.append(date.strftime('%b %d'))
    
    # Facility performance - Top 5 facilities
    facilities_data = db.session.query(
        Facility.name,
        func.count(Appointment.id).label('appt_count')
    ).join(Appointment, Appointment.facility_id == Facility.id, isouter=True)\
     .filter(Facility.is_active == True)\
     .group_by(Facility.id, Facility.name)\
     .order_by(func.count(Appointment.id).desc())\
     .limit(5).all()
    
    facility_names = [f.name for f in facilities_data] if facilities_data else [
        'City Hospital', 'Rural Health Center', 'District PHC', 'Community Clinic', 'Primary Care Center'
    ]
    facility_counts = [f.appt_count for f in facilities_data] if facilities_data else [
        145, 98, 87, 76, 65
    ]
    
    # District-wise distribution
    district_data = db.session.query(
        Facility.district,
        func.count(Appointment.id).label('count')
    ).join(Appointment, Appointment.facility_id == Facility.id, isouter=True)\
     .filter(Facility.district.isnot(None))\
     .group_by(Facility.district).all()
    
    district_labels = [d.district for d in district_data] if district_data else [
        'Pune', 'Mumbai', 'Nagpur', 'Nashik', 'Aurangabad'
    ]
    district_counts = [d.count for d in district_data] if district_data else [
        450, 380, 290, 245, 185
    ]
    
    # Monthly trend (last 6 months)
    monthly_labels = []
    monthly_data = []
    for i in range(5, -1, -1):
        month_date = today - timedelta(days=30*i)
        monthly_labels.append(month_date.strftime('%b %Y'))
        # Mock increasing trend
        monthly_data.append(180 + (5-i) * 25)
    
    return jsonify({
        'appointments_timeline': {
            'labels': timeline_labels,
            'data': timeline_data
        },
        'facility_performance': {
            'labels': facility_names,
            'data': facility_counts
        },
        'district_distribution': {
            'labels': district_labels,
            'data': district_counts
        },
        'monthly_trend': {
            'labels': monthly_labels,
            'data': monthly_data
        },
        'visited_vs_non_visited': [85, 15],
        'facilities_status': [
            Facility.query.filter_by(is_active=True).count() or 15, 
            Facility.query.filter_by(is_active=False).count() or 3
        ],
        'consultation_types': {
            'labels': ['OPD', 'Diagnostic', 'Emergency', 'Follow-up'],
            'data': [45, 30, 15, 10]
        },
        'ai_performance': {
            'labels': ['Processed', 'Pending', 'Manual Review'],
            'data': [856, 98, 26]
        }
    })

@admin_bp.route('/alerts', methods=['GET'])
def get_alerts():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
    alerts = []
    
    if logs:
        for log in logs:
            alerts.append({
                'id': log.id,
                'action': log.action,
                'target_id': log.target_id,
                'details': log.details,
                'timestamp': log.timestamp.isoformat()
            })
    else:
        # Mock alerts if no real data
        now = datetime.utcnow()
        alerts = [
            {
                'id': 1,
                'action': 'USER_REGISTERED',
                'target_id': 15,
                'details': 'New patient registered: Ramesh Kumar',
                'timestamp': (now - timedelta(minutes=5)).isoformat()
            },
            {
                'id': 2,
                'action': 'APPOINTMENT_BOOKED',
                'target_id': 234,
                'details': 'Appointment booked at City Hospital',
                'timestamp': (now - timedelta(minutes=15)).isoformat()
            },
            {
                'id': 3,
                'action': 'FACILITY_REGISTERED',
                'target_id': 8,
                'details': 'New facility: Rural Health Center',
                'timestamp': (now - timedelta(hours=1)).isoformat()
            },
            {
                'id': 4,
                'action': 'USER_LOGIN',
                'target_id': 42,
                'details': 'Doctor login: Dr. Priya Sharma',
                'timestamp': (now - timedelta(hours=2)).isoformat()
            },
            {
                'id': 5,
                'action': 'FEEDBACK_SUBMITTED',
                'target_id': 156,
                'details': 'Patient feedback: 5 stars',
                'timestamp': (now - timedelta(hours=3)).isoformat()
            },
            {
                'id': 6,
                'action': 'APPOINTMENT_RESCHEDULED',
                'target_id': 189,
                'details': 'Appointment rescheduled by patient',
                'timestamp': (now - timedelta(hours=4)).isoformat()
            },
            {
                'id': 7,
                'action': 'AI_CONSULTATION_PROCESSED',
                'target_id': 267,
                'details': 'AI summary generated for consultation',
                'timestamp': (now - timedelta(hours=5)).isoformat()
            },
            {
                'id': 8,
                'action': 'FACILITY_PROFILE_UPDATED',
                'target_id': 3,
                'details': 'District PHC updated services',
                'timestamp': (now - timedelta(hours=6)).isoformat()
            }
        ]
    
    return jsonify({'alerts': alerts})
