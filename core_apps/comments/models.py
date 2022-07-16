from django.db import models
from django.contrib.auth import get_user_model

from core_apps.common.models import TimeStampedUUIDModel
from core_apps.articles.models import Article
from core_apps.users.models import User


class Comment(TimeStampedUUIDModel):
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)

    commentor = models.ForeignKey(User, related_name="commentor", on_delete=models.CASCADE)

    body = models.TextField()

    def __str__(self) -> str:
        return f"{self.commentor.username} has commented on {self.article.title}"
