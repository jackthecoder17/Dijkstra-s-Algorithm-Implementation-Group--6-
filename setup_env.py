#!/usr/bin/env python3
"""
Setup script to create .env file for the Nigerian City Distance Calculator.
"""
import os
from pathlib import Path

def create_env_file():
    """Create .env file with development settings."""
    env_content = """# Django Settings for Development
SECRET_KEY=django-insecure-city-distance-calculator-dev-key-2024
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database (using SQLite for development)
# For production, you might want to use PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/city_distance_db

# CORS Settings (for frontend integration)
CORS_ALLOW_ALL_ORIGINS=True

# Static Files
STATIC_URL=/static/
STATIC_ROOT=staticfiles
"""
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists. Backing up to .env.backup")
        env_file.rename(".env.backup")
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Created .env file with development settings")
    print("📝 You can now run: python3 start_server.py")

def main():
    """Main setup function."""
    print("🔧 Setting up environment variables...")
    create_env_file()
    
    print("\n📚 Environment Variables Created:")
    print("   SECRET_KEY: Django secret key for development")
    print("   DEBUG: True (for development)")
    print("   ALLOWED_HOSTS: localhost,127.0.0.1,0.0.0.0")
    print("   CORS_ALLOW_ALL_ORIGINS: True (for frontend)")
    
    print("\n🚀 Next Steps:")
    print("   1. Run: python3 start_server.py")
    print("   2. Test: python3 test_api.py")
    print("   3. Visit: http://localhost:8001/docs")
    
    print("\n🌐 For Vercel Deployment:")
    print("   Set these in Vercel dashboard:")
    print("   - SECRET_KEY: Generate a secure key")
    print("   - DEBUG: False")
    print("   - ALLOWED_HOSTS: your-domain.vercel.app")

if __name__ == "__main__":
    main()
