# checkout the docs  for serializers.----RelatedField -> https://www.django-rest-framework.org/api-guide/relations/
# I beleive that serializers.RelatedField is the superset of the RelatedField

from rest_framework import serializers
from django.utils.text import slugify

from .models import Tag

# making custom RelatedField to be used in serializers 
class TagRelatedField(serializers.RelatedField):    
    def get_queryset(self):
        return Tag.objects.all()
    
    def to_internal_value(self, data):
        tag, created = Tag.objects.get_or_create(tag=data, slug=slugify(data))
        return tag # returning newly created/exsisting  Tag object
    
    def to_representation(self, value):  # this will be shown in the JSON response from this field 
        return value.tag