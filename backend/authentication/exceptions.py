from rest_framework.exceptions import APIException

class CustomPermissionDenied(APIException):
    status_code = 403
    default_detail = 'You do not have permission to perform this action.'

    def __init__(self, detail: str=None, status_code: int|None=None):
        if detail is not None:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code