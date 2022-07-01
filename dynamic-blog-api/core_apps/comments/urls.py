from django.urls import path

from .views import CommentAPIView, CommentUpdateDeleteAPIView

urlpatterns = [
    path('comment/<slug:slug>', CommentAPIView.as_view(), name="add-comment"),
    path('comment/<slug:slug>/<int:id>', CommentUpdateDeleteAPIView.as_view(), name='edit-comment'),
]