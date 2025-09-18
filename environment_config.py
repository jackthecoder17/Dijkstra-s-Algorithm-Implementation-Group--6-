"""
Environment configuration for Nigerian City Distance Calculator.
Copy this to .env file or set these as environment variables.
"""

# =============================================================================
# DEVELOPMENT ENVIRONMENT VARIABLES
# =============================================================================
# Copy these to a .env file in your project root:

DEVELOPMENT_ENV = """
# Django Settings for Development
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

# =============================================================================
# PRODUCTION ENVIRONMENT VARIABLES (for Vercel)
# =============================================================================
# Set these in your Vercel dashboard:

PRODUCTION_ENV = """
# Production Settings (set in Vercel dashboard)
SECRET_KEY=your-super-secret-production-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.vercel.app

# Database (if using external database)
# DATABASE_URL=postgresql://user:pass@host:port/dbname

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=True
"""

# =============================================================================
# ENVIRONMENT VARIABLE EXPLANATIONS
# =============================================================================

ENV_EXPLANATIONS = {
    "SECRET_KEY": {
        "description": "Django secret key for cryptographic signing",
        "development": "django-insecure-city-distance-calculator-dev-key-2024",
        "production": "Generate a secure random key for production",
        "required": True
    },
    "DEBUG": {
        "description": "Enable/disable debug mode",
        "development": "True",
        "production": "False",
        "required": True
    },
    "ALLOWED_HOSTS": {
        "description": "Comma-separated list of allowed hostnames",
        "development": "localhost,127.0.0.1,0.0.0.0",
        "production": "your-domain.vercel.app",
        "required": True
    },
    "DATABASE_URL": {
        "description": "Database connection string (optional, defaults to SQLite)",
        "development": "Not needed (uses SQLite)",
        "production": "postgresql://user:pass@host:port/dbname",
        "required": False
    },
    "CORS_ALLOW_ALL_ORIGINS": {
        "description": "Allow CORS requests from any origin",
        "development": "True",
        "production": "True (or specify specific origins)",
        "required": False
    }
}

def print_environment_setup():
    """Print instructions for setting up environment variables."""
    print("🔧 Environment Variables Setup")
    print("=" * 50)
    print("\n📝 Create a .env file in your project root with:")
    print(DEVELOPMENT_ENV)
    print("\n🚀 For Vercel deployment, set these in Vercel dashboard:")
    print(PRODUCTION_ENV)
    print("\n📚 Environment Variable Explanations:")
    for var, info in ENV_EXPLANATIONS.items():
        print(f"\n{var}:")
        print(f"  Description: {info['description']}")
        print(f"  Development: {info['development']}")
        print(f"  Production: {info['production']}")
        print(f"  Required: {'Yes' if info['required'] else 'No'}")

if __name__ == "__main__":
    print_environment_setup()
