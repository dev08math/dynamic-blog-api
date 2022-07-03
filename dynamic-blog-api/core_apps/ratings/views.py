# using api_view decorators for handling  API requests

import re
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes  # rest_framwork.decorators doesn't have a decorator for serializer_class
from rest_framework.response import Response

from core_apps.articles.models import Article

from .exceptions import CantRateYourArticle, NotYourRating
from .models import Rating


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])   

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
        rating = Rating.objects.create(
            article=article,
            critic=request.user,
            value=data["value"],
            review=data["review"],
        )
        return Response({"success": "Your rating has been added"}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
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
        if(request.data["value"]): rated_obj.value = request.data["value"]
        if(request.data["review"]) : rated_obj.review = request.data["review"]
        rated_obj.save()

        return Response({"success" : "Your rating has been successfully changed"}, status=status.HTTP_200_OK)