from django.db import models

from config.settings import redis_page_cache


class Page(models.Model):
    url = models.URLField(max_length=255, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True)

    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = (("title"), )


class Topic(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True)
