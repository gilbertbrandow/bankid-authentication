from rest_framework.response import Response
from rest_framework.request import Request
from .permissions import HasPermission
from .views_base import CustomAPIView
from typing import Callable, Type
from rest_framework import status
from django.db import models
from functools import wraps

def get_and_check_object_permissions(model: Type[models.Model]) -> Callable:
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _wrapped_view(view: CustomAPIView, request: Request, pk: int) -> any:
            try:
                obj = model.objects.get(pk=pk)
            except model.DoesNotExist:
                return Response(data={'detail': f'{model.__name__} not found.'}, status=status.HTTP_404_NOT_FOUND)
            view.check_object_permissions(request=request, obj=obj)
            return view_func(view, request, obj)
        return _wrapped_view
    return decorator


def check_permission(permission_codename: str) -> Callable:
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _wrapped_view(view: CustomAPIView, request: Request, *args, **kwargs) -> any:
            permission_checker = HasPermission(permission_codename=permission_codename)
            permission_checker.has_permission(request, view)
            return view_func(view, request, *args, **kwargs)
        return _wrapped_view
    return decorator