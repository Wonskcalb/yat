from django.contrib import admin
from django.contrib.admin import register

from . import models


@register(models.Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title", "description")
