# using api_view decorators for handling  API requests

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, serializer_class
from rest_framework.response import Response

from core_apps.articles.models import Article

from .exceptions import CantRateYourArticle, NotYourRating
from .models import Rating
from .serializers import RatingSerializers

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@serializer_class([RatingSerializers])
def create_article_rating(request, article_id):
    author = request.user
    article = Article.objects.get(id=article_id)
    data = request.data

    if article.author == author:
        raise CantRateYourArticle
    
    if data["value"] == 0:
        formatted_response = {'detail' : "You can't rate an article's rating as 0"}
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = RatingSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
@serializer_class([RatingSerializers])
def edit_article_rating(request, rating_id):
    editor = request.user  # have to see whether to give user obj or username 
    rated_obj = Rating.objects.get(id=rating_id)
    data = request.data

    if rated_obj.critic != editor:
        raise NotYourRating
    
    if data["value"] == 0:
        formatted_response = {'detail' : "You can't rate an article's rating as 0"}
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = RatingSerializers(instance=rated_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)