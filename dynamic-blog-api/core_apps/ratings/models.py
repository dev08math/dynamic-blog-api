from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()

class Rating(TimeStampedUUIDModel):
    class Range(models.IntegerChoices):   # helps in code reusability( DRY coding)
        RATING_1 = 1, _("Poor")
        RATING_2 = 2, _("Fair")
        RATING_3 = 3, _("Good")
        RATING_4 = 4, _("Very Good")
        RATING_5 = 5, _("Excellent")
    # Now if I want to use a DS like 'Range' I can just like directly import this class instead of wrting a new one

    article = models.ForeignKey(to="articles.Article", related_name="article_ratings", on_delete=models.CASCADE)

    critic = models.ForeignKey(User, related_name="user_who_rated", on_delete=models.CASCADE)

    value = models.IntegerField(verbose_name=_("Value"), default=0, choices=Range.choices, help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent")

    review = models.TextField(verbose_name=_("Review"), blank = True)

    class Meta:
        verbose_name_plural = "Ratings"
        unique_together = ["critic", "article"]  # have to figure this one out
    
    def __str__(self):
        return f"{self.article.title} is rated at {self.value}"
