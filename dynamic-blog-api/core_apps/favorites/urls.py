from django.urls import path

from . import views

urlpatterns = [
    path(
        "my_favorites/",
        views.ListUserFavoriteArticlesAPIView.as_view(),
        name="my-favorites",
    ),
    path("<slug:slug>/", views.FavoriteAPIView.as_view(), name="favorite-article"),
]
