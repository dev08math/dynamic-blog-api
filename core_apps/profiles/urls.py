from django.urls import path

from .views import (
    FollowUnfollowAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    UpdateProfileAPIView,
    get_details,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path(
        "user/<str:username>/", ProfileDetailAPIView.as_view(), name="profile-details"
    ),
    path(
        "update/<str:username>/", UpdateProfileAPIView.as_view(), name="profile-update"
    ),
    path("details/", get_details, name="my-details"),
    path(
        "follow/<str:username>",
        FollowUnfollowAPIView.as_view(),
        name="follow-unfollow",
    ),
]