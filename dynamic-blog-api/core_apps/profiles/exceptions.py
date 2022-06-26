# APIException helps in displaying custom messages  for all exceptions raised inside an `APIView` class or `@api_view`.
from rest_framework.exceptions import APIException

class NotYourProfile(APIException):
    status_code = 403 # forbidden error for unauthorized viewing of someone else's profile
    default_detail = "You can't edit or view this profile without proper authorization"

class CantFollowSelf(APIException):
    status_code = 403
    default_detail = "Your cannot follow yourself"
