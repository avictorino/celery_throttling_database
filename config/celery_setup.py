from dotenv import load_dotenv
try:
    load_dotenv()
except:
    pass

import django
django.setup()
### DO NOT CHANGE THE IMPORT ORDER
from celery import Celery
from config import settings
celery_app = Celery()
celery_app.conf.enable_utc = True
celery_app.conf.broker_url = settings.CELERY_BROKER_URL