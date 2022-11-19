
from pathlib import Path
import os

from split_settings.tools import include
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET')


DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', '127.0.0.1')]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

include(
    'components/databases.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/password_validators.py',
    'components/logging.py'
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = '{0}/static'.format(BASE_DIR)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
