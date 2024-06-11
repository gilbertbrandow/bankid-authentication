from rest_framework.views import APIView
from rest_framework.request import Request
from .exceptions import CustomPermissionDenied

class CustomAPIView(APIView):
    def permission_denied(self, request: Request, message: CustomPermissionDenied|None=None) -> None:
        if isinstance(message, CustomPermissionDenied):
            raise CustomPermissionDenied(detail=message.detail)
        super().permission_denied(request, message)