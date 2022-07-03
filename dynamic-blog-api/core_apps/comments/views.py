from lib2to3.pgen2.token import COMMENT
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from core_apps.articles.models import Article

from .models import Comment
from .serializers import CommentSectionSerializer, CommentSerializer
from .exceptions import TamperComment

# using generics.GenericAPIViewto handle API request methods
class CommentAPIView(generics.GenericAPIView):
    permission_classes = ([permissions.IsAuthenticated])
    serializer_class = CommentSerializer
   
    def get(self, request, **kwargs): 
        try:
            slug = self.kwargs['slug']
            article = Article.objects.get(slug=slug)
        except:
            raise NotFound("No such requested article exists")
        
        try:
            comment_check = Comment.objects.filter(article__pkid = article.pkid) # accessing article pkids to compare it with the current slus's pkid
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
        
        print(request.data)
        
        data = dict()
        comment = request.data["body"]
        commentor = request.user
        obj = Comment.objects.create(article=article, body=comment, commentor=commentor)

        data["id"] = obj.pkid
        data["username"] = obj.commentor.username
        data["commented on"] = obj.article.title
        data["comment"] = obj.body
        data["commented at"] = obj.createdAt.strftime("%m/%d/%Y, %H:%M:%S")
        
        response = {"message": "Comment successfully added", "data" : data}
        status_code = status.HTTP_201_CREATED
        return Response(response, status_code)

class CommentUpdateDeleteAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer

    def put(self, request, slug, id):
        try:
            comment_to_update = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")

        user = request.user
        if comment_to_update.commentor.username != user.username:
            raise TamperComment

        data = request.data
        serializer = self.serializer_class(comment_to_update, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "Comment updated successfully",
            "comment": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def delete(self, request, slug, id):
        try:
            comment_to_delete = Comment.objects.get(id=id)  # id is the UUID not the pkid
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")

        user = request.user
        if comment_to_delete.commentor.username != user.username:
            raise TamperComment

        comment_to_delete.delete()
        response = {"message": "Comment deleted successfully"}
        return Response(response, status=status.HTTP_200_OK)