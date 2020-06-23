"""
backend-challenge-001 WSGI Configuration
"""
###
# Libraries
###
import os

from django.core.wsgi import get_wsgi_application

###
# Main Configuration
###
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
application = get_wsgi_application()
