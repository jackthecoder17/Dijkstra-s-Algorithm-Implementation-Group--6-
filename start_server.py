#!/usr/bin/env python
"""
Startup script for the Nigerian City Distance Calculator API.
This script initializes the database and starts both Django and FastAPI servers.
"""
import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def start_django_server():
    """Start Django development server."""
    print("🚀 Starting Django REST Framework server on http://localhost:8000")
    os.system("python3 manage.py runserver 8000")

def start_fastapi_server():
    """Start FastAPI server."""
    print("🚀 Starting FastAPI server on http://localhost:8001")
    os.system("python3 fastapi_app.py")

def main():
    """Main startup function."""
    print("🇳🇬 Nigerian City Distance Calculator API")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip3 install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Run migrations
    if not run_command("python3 manage.py makemigrations", "Creating migrations"):
        print("⚠️  Warning: Migration creation failed, but continuing...")
    
    if not run_command("python3 manage.py migrate", "Running migrations"):
        print("❌ Failed to run migrations. Please check your database configuration.")
        sys.exit(1)
    
    # Populate database with Nigerian cities
    print("🏙️  Populating database with Nigerian cities...")
    if not run_command("python3 manage.py populate_nigerian_cities", "Populating database"):
        print("⚠️  Warning: Database population failed, but continuing...")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📚 Available endpoints:")
    print("   Django REST API: http://localhost:8000/api/")
    print("   FastAPI Docs:    http://localhost:8001/docs")
    print("   Django Admin:    http://localhost:8000/admin/")
    
    print("\n🚀 Starting servers...")
    print("   Press Ctrl+C to stop both servers")
    
    # Start both servers in separate threads
    django_thread = threading.Thread(target=start_django_server)
    fastapi_thread = threading.Thread(target=start_fastapi_server)
    
    django_thread.daemon = True
    fastapi_thread.daemon = True
    
    django_thread.start()
    time.sleep(2)  # Give Django a moment to start
    fastapi_thread.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
