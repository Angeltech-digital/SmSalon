"""
WSGI config for salon_project.
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise  # <-- add this

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_project.settings')

application = get_wsgi_application()

# Serve static files with WhiteNoise
application = WhiteNoise(application, root=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles'))
