"""
Database Migration Script
Run this to update the database schema with new authentication fields
"""
from app import create_app
from models import db
from sqlalchemy import text

def migrate_database():
    """Add new columns to existing tables"""
    app = create_app()
    
    with app.app_context():
        print("Starting database migration...")
        
        try:
            # Add new columns to users table
            with db.engine.connect() as conn:
                # Check if columns exist before adding
                result = conn.execute(text("PRAGMA table_info(users)"))
                columns = [row[1] for row in result]
                
                if 'mobile' not in columns:
                    print("Adding 'mobile' column to users table...")
                    conn.execute(text("ALTER TABLE users ADD COLUMN mobile VARCHAR(15)"))
                    conn.commit()
                
                if 'is_mobile_verified' not in columns:
                    print("Adding 'is_mobile_verified' column to users table...")
                    conn.execute(text("ALTER TABLE users ADD COLUMN is_mobile_verified BOOLEAN DEFAULT 0"))
                    conn.commit()
                
                if 'is_email_verified' not in columns:
                    print("Adding 'is_email_verified' column to users table...")
                    conn.execute(text("ALTER TABLE users ADD COLUMN is_email_verified BOOLEAN DEFAULT 0"))
                    conn.commit()
                
                if 'is_active' not in columns:
                    print("Adding 'is_active' column to users table...")
                    conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                    conn.commit()
                
                if 'last_login' not in columns:
                    print("Adding 'last_login' column to users table...")
                    conn.execute(text("ALTER TABLE users ADD COLUMN last_login DATETIME"))
                    conn.commit()
                
                # Make email and password_hash nullable
                print("Updating users table constraints...")
                
                # Add mobile column to patients table
                result = conn.execute(text("PRAGMA table_info(patients)"))
                columns = [row[1] for row in result]
                
                if 'mobile' not in columns:
                    print("Adding 'mobile' column to patients table...")
                    conn.execute(text("ALTER TABLE patients ADD COLUMN mobile VARCHAR(15)"))
                    conn.commit()
                
                # Add mobile column to doctors table
                result = conn.execute(text("PRAGMA table_info(doctors)"))
                columns = [row[1] for row in result]
                
                if 'mobile' not in columns:
                    print("Adding 'mobile' column to doctors table...")
                    conn.execute(text("ALTER TABLE doctors ADD COLUMN mobile VARCHAR(15)"))
                    conn.commit()
            
            # Create OTP verifications table if it doesn't exist
            print("Creating otp_verifications table...")
            db.create_all()
            
            print("\n✅ Database migration completed successfully!")
            print("\nNext steps:")
            print("1. Test the authentication endpoints")
            print("2. Update frontend to use new mobile-based auth")
            print("3. Configure SMS gateway for production")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {str(e)}")
            print("You may need to backup and recreate the database.")
            print("\nTo recreate database:")
            print("1. Backup existing data")
            print("2. Delete vitalis.db")
            print("3. Run the application to create fresh tables")

if __name__ == '__main__':
    migrate_database()
