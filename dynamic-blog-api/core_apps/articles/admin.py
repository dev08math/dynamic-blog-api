from django.contrib import admin

from .models import Tag, Article, ArticleViews


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pkid", "author", "slug", "article_read_time", "views"]   # can access getter methods in this, but not the case of fields in ModelFroms or ModelSerializers etc..
    list_display_links = ["pkid", "author"]


admin.site.register(Article, ArticleAdmin)

admin.site.register(Tag)

admin.site.register(ArticleViews)