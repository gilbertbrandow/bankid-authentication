from rest_framework.response import Response
from rest_framework.request import Request
from .permissions import HasPermissionOrIsSuperuser, IsSuperuser
from .views_base import CustomAPIView
from typing import Callable, Type
from rest_framework import status
from django.db import models
from functools import wraps
from typing import Any


def get_and_check_object_permissions(model: Type[models.Model]) -> Callable:
    """
    Decorator that retrieves an object by its primary key and checks if the user has 
    the required object-level permissions.

    :param model: The Django model class of the object to retrieve and check permissions for.
    :return: The decorated view function.
    """
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _wrapped_view(view: CustomAPIView, request: Request, pk: int, *args: Any, **kwargs: Any) -> Any:
            try:
                obj = model.objects.get(pk=pk)
            except model.DoesNotExist:
                return Response(data={'detail': f'{model.__name__} not found.'}, status=status.HTTP_404_NOT_FOUND)

            view.check_object_permissions(request=request, obj=obj)
            return view_func(view, request, obj, *args, **kwargs)
        return _wrapped_view
    return decorator


def check_permission(permission_codename: str) -> Callable:
    """
    Decorator that checks if the user has the specified permission or is a superuser.

    :param permission_codename: The codename of the required permission.
    :return: The decorated view function.
    """
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _wrapped_view(view: CustomAPIView, request: Request, *args: Any, **kwargs: Any) -> Any:
            permission_checker: HasPermissionOrIsSuperuser = HasPermissionOrIsSuperuser(permission_codename=permission_codename)
            permission_checker.has_permission(request, view)
            return view_func(view, request, *args, **kwargs)
        return _wrapped_view
    return decorator


def check_superuser_permission() -> Callable:
    """
    Decorator that checks if the user is a superuser.

    :return: The decorated view function.
    """
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _wrapped_view(view: CustomAPIView, request: Request, *args: Any, **kwargs: Any) -> Any:
            superuser_checker = IsSuperuser()
            superuser_checker.has_permission(request, view)
            return view_func(view, request, *args, **kwargs)
        return _wrapped_view
    return decorator
