from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.articles.models import Article
from core_apps.articles.serializers import ArticleSerializer

from .exceptions import AlreadyInFavorites
from .models import Favorite
from .serializers import FavoriteSerializer

class FavoritesView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def post(self, request, slug):
        article = Article.objects.get(slug=slug)
        user = request.user
        data = request.data
        favorite = Favorite.objects.filter(article=article, user=user)

        if favorite:
            raise AlreadyInFavorites
        else:
            data["article"] = article.pkid  
            data["user"] = user.pkid
            serializer = self.get_serializer(data=data) # accesses the serializer_class
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ListUserFavoriteArticles(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favtorites = Favorite.objects.filter(user=request.user)  # testing

        favorite_articles = [ ArticleSerializer(f.article).data["title"] for f in favtorites]

        my_favorites = { "my_favorites" : favorite_articles}

        return Response(data=my_favorites, status=status.HTTP_200_OK)