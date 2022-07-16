from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

from core_apps.articles.models import Article
from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()

class Favorite(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="favorite_articles"
    )

    def __str__(self):
        return f"{self.user.username} has added {self.article.title} in favorites"
    
    def is_favorited(self, user, article):
        try:
            article = self.article
            user = self.user
        except Article.DoesNotExist:
            raise NotFound("It seems like that the article has been removed or blocked.")

        queryset = Favorite.objects.filter(article__id=article.id, user__id=user.id)

        if queryset:
            return True
        return False
