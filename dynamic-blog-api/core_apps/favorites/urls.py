from django.urls import path

from . import views

urlpatterns = [
    path(
        "my_favorites/",
        views.ListUserFavoriteArticles.as_view(),
        name="my-favorites",
    ),
    path("<slug:slug>/", views.FavoritesView.as_view(), name="favorite-article"),
]
