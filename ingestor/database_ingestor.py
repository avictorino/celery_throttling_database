from core.models import Page, Topic


class DatabaseIngestor:

    def __init__(self, page: dict):
        self._page = page

    def execute(self):

        page = Page.objects.create(
            title=self._page["title"],
            description=self._page["description"],
            url=self._page["url"]
        )

        topics = [Topic(title=t["title"], description=t["description"], page=page)
                  for t in self._page["topics"]]

        Topic.objects.bulk_create(topics)
        print(f'Page {self._page["title"]} inserted with: {len(topics)} topics')
