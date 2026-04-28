import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-fallback'
    
    # Render sets DATABASE_URL automatically if we add a Postgres DB, but we're strictly SQLite.
    # So we'll use a local SQLite path or an environment variable.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///vitalis.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads path
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
