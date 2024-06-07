"""
URL configuration for authentication.

"""

from django.urls import path
from .views import UserList, AccountList

urlpatterns = [
    path('users', UserList.as_view(), name='users'),
    path('accounts', AccountList.as_view(), name='accounts'),
]
