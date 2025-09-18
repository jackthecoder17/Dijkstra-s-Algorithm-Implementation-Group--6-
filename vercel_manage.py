#!/usr/bin/env python
"""Vercel-specific Django management script."""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Set Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'city_distance_calculator.settings_production')

# Setup Django
django.setup()

def application(environ, start_response):
    """WSGI application for Vercel."""
    from django.core.wsgi import get_wsgi_application
    return get_wsgi_application()(environ, start_response)

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
