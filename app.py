from flask import Flask, jsonify, send_from_directory, render_template
from flask_cors import CORS
from config import Config
from models import db
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Initialize SQLAlchemy
    db.init_app(app)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register Blueprints
    from routes.auth import auth_bp
    from routes.patient import patient_bp
    from routes.doctor import doctor_bp
    from routes.asha import asha_bp
    from routes.admin import admin_bp
    from routes.cis import cis_bp
    from routes.health import health_bp
    from routes.facility import facility_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(asha_bp, url_prefix='/api/asha')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(cis_bp, url_prefix='/api/cis')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(facility_bp, url_prefix='/api/facility')

    # Frontend routes (Pages)
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login_redirect():
        return render_template('login.html')
    
    @app.route('/register')
    def register_redirect():
        return render_template('register.html')

    @app.route('/patient')
    def patient_dashboard():
        return render_template('patient_dashboard.html')

    @app.route('/doctor')
    def doctor_dashboard():
        return render_template('doctor_dashboard.html')

    @app.route('/asha')
    def asha_dashboard():
        return render_template('asha_dashboard.html')

    @app.route('/admin')
    def admin_dashboard():
        return render_template('admin_dashboard.html')

    @app.route('/facility')
    def facility_dashboard():
        return render_template('facility_dashboard.html')

    @app.route('/crm')
    def crm_dashboard():
        return render_template('crm_dashboard.html')

    @app.route('/feedback')
    def feedback_module():
        return render_template('feedback_module.html')

    # Tool HTML Routes
    @app.route('/doctor/tools/risk-assessment')
    def tool_risk_assessment():
        return render_template('tools/risk_assessment.html')

    @app.route('/doctor/tools/shap')
    def tool_shap():
        return render_template('tools/shap_analysis.html')

    @app.route('/doctor/tools/visual-scan')
    def tool_visual_scan():
        return render_template('tools/visual_intelligence.html')

    @app.route('/doctor/tools/rag-assistant')
    def tool_rag_assistant():
        return render_template('tools/rag_assistant.html')

    @app.route('/doctor/tools/chatbot')
    def tool_chatbot():
        return render_template('tools/ai_chatbot.html')

    @app.route('/doctor/tools/prescription')
    def tool_prescription():
        return render_template('tools/prescription_engine.html')

    @app.route('/doctor/tools/three-layer-explanation')
    def tool_three_layer():
        return render_template('tools/three_layer_explanation.html')

    @app.route('/doctor/tools/analytics')
    def tool_analytics():
        return render_template('tools/analytics.html')

    # Create tables
    with app.app_context():
        db.create_all()
        # You could also add basic seed data here if the DB is empty

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
