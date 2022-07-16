from rest_framework.exceptions import APIException


class CantRateYourArticle(APIException):
    status_code = 403
    default_detail = "You can't rate/review your own article"

class NotYourRating(APIException):
    status_code = 403
    default_detail = "You can't edit someone else's rating"