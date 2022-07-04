from rest_framework.exceptions import APIException


class AlreadyInFavorites(APIException):
    status_code = 400
    default_detail = "This article is aready in your favorites"