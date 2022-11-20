from pathlib import Path
import os

from django.core.wsgi import get_wsgi_application
import dotenv

dotenv.read_dotenv(
    os.path.join(
        Path(__file__).resolve().parent.parent, '.env'
    )
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
