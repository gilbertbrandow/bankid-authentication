from rest_framework.views import APIView
from rest_framework.request import Request
from .exceptions import PermissionDenied

class CustomAPIView(APIView):
    def permission_denied(self, request: Request, message: PermissionDenied|None=None) -> None:
        if isinstance(message, PermissionDenied):
            raise PermissionDenied(detail=message.detail)
        super().permission_denied(request, message)