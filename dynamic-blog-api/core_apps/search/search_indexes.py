from xml.dom.minidom import Document
from django.utils import timezone
from haystack import indexes

from core_apps.articles.models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    author = indexes.CharField(model_attr="author") # needs to be a proper model attribute
    title  = indexes.CharField(model_attr = "title")
    body = indexes.CharField(model_attr = "body")
    created_at = indexes.CharField(model_attr="createdAt")
    updated_at = indexes.CharField(model_attr="updatedAt")

    @staticmethod
    def prepare_author(obj):  # special staticmethod for 'author',  to override the way the specific index is presented
        return "" if not obj.author else obj.username # return username is the author exists

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((obj.author.username, obj.title, obj.description))
    
    def get_model(obj): # sets the model 
        return Article
    
    def index_queryset(self, using=None): # returns the queryset of all the article created till now
        return self.get_model().objects.filter(createdAt__at__lte=timezone.now())

    # have to check whether autocomplete actually works