from django.urls import path

from .views import create_article_rating, edit_article_rating

urlpatterns = [
    path("<str:article_id>", create_article_rating, name = "create-rating"),
    path("update/<str:rating_id>", edit_article_rating, name = "edit-rating"),
]