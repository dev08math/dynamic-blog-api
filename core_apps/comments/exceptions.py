from rest_framework.exceptions import APIException

class TamperComment(APIException):
    status_code = 403
    default_detail = "You can't edit/update a comment that does not belong to you"