import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the parent directory to the Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_settings.settings')

application = get_wsgi_application()