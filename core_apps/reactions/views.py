from amqp import NotFound
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from core_apps.articles.models import Article

from .models import Reaction


def find_article_obj(slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise NotFound(f"Article with the slug {slug} does not exist.")
    return article

class ReactionAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def set_reaction(self, user, article, reaction):
        try:
            existing_reaction = Reaction.objects.get(article=article, user=user)
            existing_reaction.delete()     # deleting the existing reaction before editing
        except Reaction.DoesNotExist:
            pass

        Reaction.objects.create(user=user, article=article, reaction = reaction)

        response = {"message": "Reaction successfully set"}
        status_code = status.HTTP_201_CREATED
        return response, status_code
    
    def post(self, request, slug):
        article = find_article_obj(slug)
        reaction = request.data.get('reaction') # whether liked or disliked

        try:
            existing_same_reaction = Reaction.objects.get(
            article=article, user=request.user, reaction=reaction
            )
            existing_same_reaction.delete()
            response = {
                "message": f"You no longer {'LIKE' if reaction in [1,'1'] else 'DISLIKE'} {article.title}"
            }
            status_code = status.HTTP_200_OK

        except Reaction.DoesNotExist:
            response, status_code = self.set_reaction(article=article, user=request.user, reaction=reaction)

        return Response(response, status_code)

