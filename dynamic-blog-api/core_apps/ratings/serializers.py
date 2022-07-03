from rest_framework import serializers

from .models import Rating

class RatingSerializers(serializers.ModelSerializer):
    rated_by = serializers.SerializerMethodField(read_only = True)
    article = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Rating
        fields = ['id', 'article', 'rated_by', 'value', 'review']

    # remember, the obj passed in a Modelserializer class' getter or setter methods is the model obj itself 
    def get_rated_by(self, obj):   
        return obj.critic.username
    
    def get_article(self, obj):
        return obj.article.title
