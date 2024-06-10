from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from rest_framework.views import APIView

class IsAuthenticated(BasePermission): 
    """
    Base permission to only allow authenticated users.
    """
    @staticmethod
    def has_permission(request: Request, view: 'Type[APIView]') -> bool:
        return request.user and request.user.is_authenticated

class IsSuperuser(BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """
    @staticmethod
    def has_permission(request: Request, view: 'Type[APIView]') -> bool:
        return request.user and request.user.is_superuser