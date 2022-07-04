from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "user", "article"]
        extra_kwargs = { "message" : "The artcile has been added tp favorites"} # have to test