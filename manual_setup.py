#!/usr/bin/env python3
"""
Manual setup script for the Nigerian City Distance Calculator.
Run this step by step if the automatic setup fails.
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and show the result."""
    print(f"\n🔄 {description}...")
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Manual setup steps."""
    print("🇳🇬 Nigerian City Distance Calculator - Manual Setup")
    print("=" * 60)
    
    print("\n📋 Setup Steps:")
    print("1. Install Python dependencies")
    print("2. Create database migrations")
    print("3. Run database migrations")
    print("4. Populate database with Nigerian cities")
    print("5. Start the servers")
    
    # Step 1: Install dependencies
    if not run_command("pip3 install -r requirements.txt", "Installing Python dependencies"):
        print("\n❌ Failed to install dependencies.")
        print("💡 Try: pip3 install --user -r requirements.txt")
        return False
    
    # Step 2: Create migrations
    if not run_command("python3 manage.py makemigrations", "Creating database migrations"):
        print("\n⚠️  Migration creation failed, but continuing...")
    
    # Step 3: Run migrations
    if not run_command("python3 manage.py migrate", "Running database migrations"):
        print("\n❌ Database migration failed.")
        return False
    
    # Step 4: Populate database
    if not run_command("python3 manage.py populate_nigerian_cities", "Populating database with Nigerian cities"):
        print("\n⚠️  Database population failed, but continuing...")
    
    print("\n🎉 Setup completed!")
    print("\n🚀 To start the servers, run:")
    print("   python3 start_server.py")
    print("\n📚 Or start them manually:")
    print("   Terminal 1: python3 manage.py runserver 8000")
    print("   Terminal 2: python3 fastapi_app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")
