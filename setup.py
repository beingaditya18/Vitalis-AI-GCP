"""
Vitalis AI - Quick Setup Script
Automates initial setup and configuration
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is 3.8+"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_pip():
    """Check if pip is installed"""
    print("\nChecking pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip is not installed")
        return False

def create_env_file():
    """Create .env file from .env.example"""
    print("\nSetting up environment variables...")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists")
        response = input("   Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("   Skipping .env creation")
            return True
    
    if os.path.exists('.env.example'):
        with open('.env.example', 'r') as src:
            content = src.read()
        
        with open('.env', 'w') as dst:
            dst.write(content)
        
        print("✅ Created .env file")
        print("⚠️  Please edit .env and add your API keys:")
        print("   - SECRET_KEY (generate a random string)")
        print("   - GEMINI_API_KEY (get from Google AI Studio)")
        return True
    else:
        print("⚠️  .env.example not found, creating basic .env")
        with open('.env', 'w') as f:
            f.write("SECRET_KEY=change-this-to-random-string\n")
            f.write("DATABASE_URL=sqlite:///vitalis.db\n")
            f.write("GEMINI_API_KEY=your-gemini-api-key-here\n")
        print("✅ Created basic .env file")
        return True

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                      check=True)
        print("\n✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Failed to install dependencies")
        return False

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    directories = [
        'static/uploads',
        'instance'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}")
    
    return True

def initialize_database():
    """Initialize database"""
    print("\nInitializing database...")
    
    response = input("Initialize database now? (Y/n): ").strip().lower()
    if response == 'n':
        print("⚠️  Skipping database initialization")
        print("   Run 'python app.py' later to initialize")
        return True
    
    try:
        from app import create_app
        from models import db
        
        app = create_app()
        with app.app_context():
            db.create_all()
        
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {str(e)}")
        print("   You can initialize it later by running: python app.py")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")
    
    print("Next steps:\n")
    print("1. Edit .env file and add your API keys:")
    print("   - SECRET_KEY (generate a random string)")
    print("   - GEMINI_API_KEY (get from https://makersuite.google.com/app/apikey)")
    print()
    print("2. Start the application:")
    print("   python app.py")
    print()
    print("3. Access the application:")
    print("   http://localhost:5000")
    print()
    print("4. Test authentication:")
    print("   python test_auth.py")
    print()
    print("5. Read documentation:")
    print("   - README.md - General documentation")
    print("   - AUTH_GUIDE.md - Authentication guide")
    print()
    print("For production deployment:")
    print("- Configure SMS gateway in services/mock_notifications.py")
    print("- Set up proper SECRET_KEY")
    print("- Consider using PostgreSQL instead of SQLite")
    print()

def main():
    """Main setup function"""
    print_header("Vitalis AI - Setup Script")
    
    print("This script will help you set up Vitalis AI\n")
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Creating environment file", create_env_file),
        ("Installing dependencies", install_dependencies),
        ("Creating directories", create_directories),
        ("Initializing database", initialize_database),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {str(e)}")
        sys.exit(1)
