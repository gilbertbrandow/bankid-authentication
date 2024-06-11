from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from typing import Type, TYPE_CHECKING
from authentication.models import Account
from django.db import models

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


class IsSameAccountOrIsSuperuser(BasePermission):
    """
    Custom permission to allow access if the  the resource is connected to the same account as the user 
    or the user is a superuser.
    """

    def has_object_permission(self, request: Request, view: 'Type[APIView]', obj: 'Type[models.Model]') -> bool:

        if request.user.is_superuser:
            return True
        
        if isinstance(obj, Account):
            return request.user.is_authenticated and obj == request.user.account

        return request.user.is_authenticated and hasattr(obj, 'account') and obj.account == request.user.account

class HasPermission(BasePermission):
    """
    Custom permission to allow access if the user has the specified permission.
    """
    def __init__(self, permission_codename: str) -> None:
        self.permission_codename = permission_codename

    def has_permission(self, request: Request, view: 'Type[APIView]') -> bool:
        user = request.user
        
        if not user or not user.is_authenticated:
            return False

        return any(permission.codename == self.permission_codename for permission in user.permissions)
