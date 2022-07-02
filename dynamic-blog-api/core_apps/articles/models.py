from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg
from django.contrib.auth import get_user_model

from core_apps.common.models import TimeStampedUUIDModel
from core_apps.ratings.models import Rating

from .read_time_engine import ArticleReadEngine

from autoslug import AutoSlugField

User = get_user_model()

def upload_to(instance, filename):
    filename = str(instance.id) + filename
    return 'banner_images/{filename}'.format(filename=filename)

class Tag(TimeStampedUUIDModel):
    tag = models.CharField(max_length=20)
    slug = models.SlugField(db_index=True, unique=True)

    class Meta:
        verbose_plural = "Tags"
    
    def __str__(self):
        return self.tag
    
class Article(TimeStampedUUIDModel):
    author = models.ForeignKey(User, verbose_name=_("Author"), related_name="articles", on_delete=models.CASCADE)

    title = models.CharField(verbose_name=_("Title"), max_length=50)

    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    
    description = models.CharField(verbose_name=_("Description"), max_length=150)

    body = models.TextField(verbose_name=_("Content"))

    banner_image = models.ImageField(verbose_name=_("Banner"), default="/banner_default.png", upload_to = upload_to)

    tags = models.ManyToManyField(Tag, related_name="articles")

    views = models.IntegerField(verbose_name=_("Article's views"), default=0)

    def __str__(self) -> str:
        return f"{self.author}'s article"
    
    def list_of_tags(self):
        tag_list= [relation.tag for relation in self.tags.all()] # tags.all() will give the list of all tags that are in relationship with  Tag class
        return tag_list
    
    def article_read_time(self):
        time_to_read = ArticleReadEngine(self)   # self is the current article obj
        return time_to_read
        
    @property
    def get_average_rating(self):
        if Rating.objects.all() > 0:
            rating = Rating.objects.filter(article=self.pkid).all().aggregate(Avg("value")) # rating will now be a single obj
            return round(rating['value__avg'],1) if rating['value__avg'] else 0
        return 0

    
class ArticleViews(TimeStampedUUIDModel):
    ip = models.CharField(max_length=38, verbose_name=_("IP Address"))
    article = models.ForeignKey(Article, verbose_name=_("Views"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.article.title} is having {self.article.views} view(s)."
    
    class Meta:
        verbose_name = "Total views on Article"
        verbose_name_plural = "Total Article Views"
