from rest_framework.permissions import BasePermission
from .exceptions import PermissionDenied
from rest_framework.request import Request
from authentication.models import Account
from typing import Type, TYPE_CHECKING
from django.db import models
from authentication.models import Permission

if TYPE_CHECKING:
    from rest_framework.views import APIView


class IsAuthenticated(BasePermission):
    """
    Base permission to only allow authenticated users.
    """
    @staticmethod
    def has_permission(request: Request, view: 'Type[APIView]') -> bool:
        if request.user and request.user.is_authenticated:
            return True
        raise PermissionDenied(detail='You must be signed in to perform this action.')


class IsSuperuser(BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """
    @staticmethod
    def has_permission(request: Request, view: 'Type[APIView]') -> bool:
        if request.user.is_superuser:
            return True
        raise PermissionDenied(detail='You must have superuser privileges to perform this action.')


class IsSameAccountOrIsSuperuser(BasePermission):
    """
    Custom permission to allow access if the resource is connected to the same account as the user
    or the user is a superuser.
    """

    def has_object_permission(self, request: Request, view: 'Type[APIView]', obj: 'Type[models.Model]') -> bool:
        user = request.user
        if user.is_superuser:
            return True
        if user.is_authenticated and isinstance(obj, Account) and obj == user.account:
            return True
        if user.is_authenticated and not hasattr(obj, 'account'):
            return True
        if user.is_authenticated and hasattr(obj, 'account') and obj.account == user.account:
            return True
        raise PermissionDenied(detail='You do not have access to this resource as it is not associated with your account.')


class HasPermissionOrIsSuperuser(BasePermission):
    """
    Custom permission to allow access if the user has the specified permission.
    """

    def __init__(self, permission_codename: str) -> None:
        self.permission_codename = permission_codename

    def has_permission(self, request: Request, view: 'Type[APIView]') -> bool:
        user = request.user

        if user.is_superuser:
            return True
        if any(permission.codename == self.permission_codename for permission in user.permissions):
            return True

        permission = Permission.objects.get(codename=self.permission_codename)
        raise PermissionDenied(detail=f'You are missing required permission: "{permission.name}"')
