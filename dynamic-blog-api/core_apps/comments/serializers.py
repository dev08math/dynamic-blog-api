from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "commentor", "article", "body", "created_at", "updated_at"]

    
    def get_created_at(self, obj):
        now = obj.createdAt
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updatedAt
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date
    
class CommentSectionSerializer(serializers.ModelSerializer):
    article = serializers.ReadOnlyField(source="article.title") # remember the attribute in source has to be in the model in class Meta
    
    commentor = serializers.ReadOnlyField(source="commentor.username")

    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "commentor", "article", "body", "created_at", "updated_at"]

    
    def get_created_at(self, obj):
        now = obj.createdAt
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updatedAt
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date
    