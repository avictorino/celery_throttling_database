from config.celery_setup import celery_app
from ingestor.database_ingestor import DatabaseIngestor
from ingestor.read_page import ReadPage
from ingestor.scan_index_page import ScanIndexPage


@celery_app.task(name="scan_index_page")
def scan_index_page(url):
    ScanIndexPage(url).execute()


@celery_app.task(name="read_page")
def read_page(url):
    ReadPage(url).execute()


@celery_app.task(name="database_ingestor", rate_limit='5/s')
def database_ingestor(page_data):
    DatabaseIngestor(page_data).execute()
