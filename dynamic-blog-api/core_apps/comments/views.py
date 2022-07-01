from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from core_apps.articles.models import Article

from .models import Comment
from .serializers import CommentSectionSerializer, CommentSerializer

# using generics.GenericAPIViewto handle API request methods
class CommentAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer

    def get(self, request, **kwargs): # *kwargs will include all the request parameters, if any
        try:
            slug = request.kwargs['slug']
            article = Article.objects.get(slug=slug)
        except:
            raise NotFound("No such requested article exists")
        
        try:
            comment_check = Comment.objects.get(article_id = article.pkid)
        except:
            raise NotFound("No commments found")
        
        serializer = CommentSectionSerializer(comment_check, many=True)

        return Response(
            {"num_of_comments": len(serializer.data), "comments": serializer.data},
            status=status.HTTP_200_OK,
        )
    
    def post(self, request, **kwargs):
        try:
            slug = self.kwargs.get("slug")
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("No such requested article exists")
        
        # testing
        data = request.data
        serializer = self.serializer_class(data=data)  
        if serializer.is_valid():
            serializer.save()

        response = {"message": "Comment successfully added"}
        status_code = status.HTTP_201_CREATED
        return response, status_code

class CommentUpdateDeleteAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer

    def put(self, request, slug, id):
        try:
            comment_to_update = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")

        data = request.data
        serializer = self.serializer_class(comment_to_update, data=data, partial=True)

        # testing how the validity error is raised using this 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "message": "Comment updated successfully",
            "comment": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def delete(self, request, slug, id):
        try:
            comment_to_delete = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")

        comment_to_delete.delete()
        response = {"message": "Comment deleted successfully"}
        return Response(response, status=status.HTTP_200_OK)