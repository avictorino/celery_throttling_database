from urllib.parse import urljoin

from config import settings
from ingestor.base_ingestor import BaseIngestor


class ScanIndexPage(BaseIngestor):
    """
        Class to initialize the process, implements the abstract class to share some functionality.
    """

    def __init__(self, url):
        super().__init__(url)

    def execute(self):
        from ingestor.task import read_page

        if not self._file_exists():

            for link in self._html.find_all("a", attrs={"class": "reference internal"}):
                page_url = urljoin(self._url, link["href"]).split("#")[0]

                if not self._file_exists(page_url):
                    if settings.DEBUG:
                        read_page(page_url) ## single thread execution
                    else:
                        read_page.delay(page_url) ## multithread execution
