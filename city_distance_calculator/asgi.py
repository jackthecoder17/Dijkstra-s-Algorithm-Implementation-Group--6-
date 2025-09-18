"""
ASGI config for city_distance_calculator project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'city_distance_calculator.settings')

application = get_asgi_application()
