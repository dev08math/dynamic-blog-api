from django.contrib import admin

from . import models


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pkid", "author", "slug", "article_read_time", "views"]   # can access getter methods in this, but not the case of fields in ModelFroms or ModelSerializers etc..
    list_display_links = ["pkid", "author"]


admin.site.register(models.Article, ArticleAdmin)