from django.contrib import admin, messages
from django.utils.text import Truncator
from core.models import Page, Topic


class TopicAdmin(admin.StackedInline):
    model = Topic
    extra = 0


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields = ["title", "description"]
    list_display = ["title", "short_description"]
    inlines = [TopicAdmin]

    def short_description(self, obj):
        return Truncator(obj.description).words(10)