"""
Reset database - Creates fresh database with all tables
"""
import os
from app import create_app
from models import db

def reset_database():
    """Delete and recreate database"""
    app = create_app()
    
    with app.app_context():
        print("Resetting database...")
        
        # Drop all tables
        print("Dropping all tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating all tables...")
        db.create_all()
        
        print("\n✅ Database reset complete!")
        print("\nYou can now:")
        print("1. Start the server: python app.py")
        print("2. Register new users")
        print("3. Test the application")

if __name__ == '__main__':
    reset_database()
