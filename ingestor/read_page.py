from urllib.parse import urlparse, urljoin

from config import settings
from config.settings import redis_page_cache
from ingestor.base_ingestor import BaseIngestor


class ReadPage(BaseIngestor):

    def __init__(self, url):
        super().__init__(url)

    def execute(self):

        if not self._file_exists():
            from ingestor.task import database_ingestor, scan_index_page

            print(f"Start ReadPage: {self._url}")

            try:
                docs_content = self._html.find_all("div", attrs={"class": "section"})

                if not docs_content or len(docs_content) == 0:
                    return

                page = None
                for content in docs_content:
                    description = None
                    if content.p:
                        description = ' '.join(content.p.text.splitlines())

                    if content.h1:
                        title = content.h1.text.replace('¶', '')

                        redis_page_cache.set(self._url, title)
                        page = dict(
                            topics=[],
                            url=self._url,
                            title=title,
                            description=description
                        )
                    elif content.h2:
                        page["topics"].append(dict(
                            title=content.h2.text.replace('¶', ''),
                            description=description
                        ))

                if settings.DEBUG:
                    database_ingestor(page)
                else:
                    database_ingestor.delay(page)

                self._execute_hyperlinks()

            except Exception as ex:
                redis_page_cache.delete(self._url)

    def _execute_hyperlinks(self):

        main_url = urlparse(self._url)
        for link in self._html.find_all("a", attrs={"class": "reference internal"}):

            if link.get("href"):
                new_url = urlparse(link.get("href"))

                if main_url.netloc == new_url.netloc or link.get("href").startswith("../"):

                    new_url = urljoin(self._url, link.get("href")).split("#")[0]

                    if not self._file_exists(new_url):
                        from ingestor.task import read_page
                        if settings.DEBUG:
                            read_page(new_url)
                        else:
                            read_page.delay(new_url)
