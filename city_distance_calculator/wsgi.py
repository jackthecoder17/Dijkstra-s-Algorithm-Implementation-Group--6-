"""
WSGI config for city_distance_calculator project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'city_distance_calculator.settings')

application = get_wsgi_application()
