from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):  # overriding IsOwnerOrReadOnly
    message = {
        "You are not authorized to update or delete this article as you are not the owner."
    }

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS include 'GET', 'OPTIONS' and 'HEAD' methods
            return True
        return obj.author == request.user   # author is an Article attribute