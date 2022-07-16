import django_filters as filters

from core_apps.articles.models import Article


class ArticleFilter(filters.FilterSet):
    # making a custom filter 
    # all the custom filters below are expected to be used for Article model alone
    # the field_name is User model's firstname, accessed via author attribute of Article model(the 'model' parameter in class Meta should be Article)
    author = filters.CharFilter(field_name="author__firstname", lookup_expr="icontains")

    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    tags = filters.CharFilter(field_name="tags",
                              method="get_article_tags", 
                              lookup_expr="created_at")
    
    created_at = filters.IsoDateTimeFilter(field_name="created_at")

    updated_at = filters.IsoDateTimeFilter(field_name="updated_at")

    class Meta:
        model = Article
        fields = ["author", "title", "tags", "created_at", "updated_at"]  # field names have to be custom filters only
    
    def get_article_tags(self, queryset, tags, value):  
        tag_values = value.replace(" ", " ").split(',')
        return queryset.filter(tags__tag__in=tag_values).distinct()