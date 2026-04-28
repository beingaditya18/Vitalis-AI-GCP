from flask import Blueprint, jsonify, request
from models import db, ASHATask

asha_bp = Blueprint('asha', __name__)

@asha_bp.route('/overview', methods=['GET'])
def overview():
    return jsonify({
        'total_patients': 150,
        'high_risk_patients': 12,
        'tasks_completed': 45,
        'work_status': 'Active'
    })

@asha_bp.route('/patients', methods=['GET'])
def patients():
    return jsonify({'patients': []})

@asha_bp.route('/doctors', methods=['GET'])
def doctors():
    return jsonify({'doctors': []})

@asha_bp.route('/claims', methods=['GET'])
def claims():
    return jsonify({'claims': []})

@asha_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = ASHATask.query.all()
    return jsonify({'tasks': [{'id': t.id, 'desc': t.description, 'completed': t.is_completed} for t in tasks]})

@asha_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    task = ASHATask.query.get(task_id)
    if task:
        task.is_completed = True
        db.session.commit()
        return jsonify({'message': 'Task completed'})
    return jsonify({'error': 'Not found'}), 404

@asha_bp.route('/charts', methods=['GET'])
def charts():
    return jsonify({'chart_data': {}})
