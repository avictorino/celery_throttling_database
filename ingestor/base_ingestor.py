import logging
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from config.settings import redis_page_cache

logger = logging.getLogger(__name__)


class BaseIngestor(ABC):
    """
        Base class to implement shared functionalities
    """

    def __init__(self, url):
        self._url = url
        self._html = BaseIngestor._read_html(self._url)

    @staticmethod
    def _read_html(url):
        print(f"Reading url: {url}")
        response = requests.get(url)
        return BeautifulSoup(response.content, 'html.parser')

    def _file_exists(self, url=None):
        if not url:
            url = self._url
        return True if redis_page_cache.get(url) else False

    @abstractmethod
    def execute(self):
        """
        Abstract class
        :return:
        """
        raise NotImplemented()
