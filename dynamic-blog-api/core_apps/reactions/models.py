from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.articles.models import Article
from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()

class ReactionManager(models.Manager):   # custom model manager for 'Reaction'

    def likes(self):
        return self.get_queryset().filter(reaction__gt=0).count()

    def dislikes(self):
        return self.get_queryset().filter(reaction__lt=0).count()
    
    def has_reacted(self):
        request = self.context['request']
        if request:
            return self.get_queryset.filter(user=request.user)
    

class Reaction(TimeStampedUUIDModel):
    class reactions(models.IntegerChoices):
        LIKE = 1, _('Like')
        DISLIKE = -1, _('Dislike')
    
    user = models.ForeignKey(User, related_name='user_who_reacted', on_delete=models.CASCADE)

    article  = models.ForeignKey(Article, related_name='article_reactions', on_delete=models.CASCADE)

    reaction = models.IntegerField(verbose_name=_('Likes&Dislikes'), choices=reactions.choices)

    objects = ReactionManager()

    class Meta:
        unique_together = ['user', 'article', 'reaction']

    def __str__(self) -> str:
        return f"{self.user.username} reacted with a {self.reaction} on {self.article.title}"