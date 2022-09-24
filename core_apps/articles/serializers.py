from rest_framework import serializers
from django.db.models import Avg

from core_apps.articles.models import Article, ArticleViews
from core_apps.comments.serializers import CommentSectionSerializer
from core_apps.ratings.serializers import RatingSerializers

from .custom_tag_field import TagRelatedField

class ArticleViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleViews
        exclude = ['updated_at', 'pkid']
    
class ArticleSerializer(serializers.ModelSerializer):

    author_info = serializers.SerializerMethodField(read_only=True)

    read_time = serializers.ReadOnlyField(source="article_read_time") 

    ratings = serializers.SerializerMethodField()

    num_ratings = serializers.SerializerMethodField()

    average_rating = serializers.SerializerMethodField()

    likes = serializers.ReadOnlyField(source="article_reactions.likes") # article is used as a foreign key in 'article_reactions' table ( reactions model)

    dislikes = serializers.ReadOnlyField(source="article_reactions.dislikes")

    tagList = TagRelatedField(many=True, required=False, source="tags")

    comments = serializers.SerializerMethodField()

    num_comments = serializers.SerializerMethodField()

    created_at = serializers.SerializerMethodField()

    updated_at = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        if len(obj.article_ratings.all()):   # accessing ratings model using related_name 
            rating = obj.article_ratings.all().aggregate(Avg("value")) # rating will now be a single obj having value attribute
            return round(rating['value__avg'],1) if rating['value__avg'] else 0
        return 0
        
    def get_created_at(self, obj):
        now = obj.createdAt
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updatedAt
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date
    
    def get_author_info(self, obj):
        return {
            "username": obj.author.username,
            "fullname": obj.author.get_full_name, # can only access direct fields or class methods. Cannot invoke getter functions
            "about_me": obj.author.profile.about_me,
            "profile_pic": obj.author.profile.profile_pic.url,
            "email": obj.author.email,
            "twitter_handle": obj.author.profile.twitter_handle,
        }
    

    def get_ratings(self, obj):
        reviews = obj.article_ratings.all()   # getting all the article ratings pertaining to an article
        serializer = RatingSerializers(reviews, many=True)
        return serializer.data

    def get_num_ratings(self, obj):
        num_reviews = obj.article_ratings.all().count()
        return num_reviews


    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentSectionSerializer(comments, many=True)
        return serializer.data

    def get_num_comments(self, obj):
        num_comments = obj.comments.all().count()
        return num_comments

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "tagList",
            "description",
            "body",
            "banner_image",
            "read_time",
            "author_info",
            "likes",
            "dislikes",
            "ratings",
            "num_ratings",
            "average_rating",
            "views",
            "num_comments",
            "comments",
            "created_at",
            "updated_at",
        ]

class ArticleCreateSerializers(serializers.ModelSerializer):
    tags = TagRelatedField(many=True, required=False)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ["updatedAt", "pkid", "createdAt"]

    def get_created_at(self, obj):
        now = obj.createdAt
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

class ArticleUpdateSerializer(serializers.ModelSerializer):
    tags = TagRelatedField(many=True, required=False)
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
                  "title", 
                  "description",
                  "body",
                  "banner_image",
                  "tags", 
                  "updated_at",
                  ]

    def get_updated_at(self, obj):
        then = obj.updatedAt
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date