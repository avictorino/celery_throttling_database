from config.celery_setup import celery_app
from config.settings import redis_page_cache
from core.models import Page
from ingestor.task import scan_index_page

Page.objects.all().delete()
redis_page_cache.flushdb()
scan_index_page("https://docs.djangoproject.com/en/3.2/intro/overview/")