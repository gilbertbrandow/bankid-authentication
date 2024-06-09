"""
URL configuration for authentication.

"""

from django.urls import path
from .views import UserList, AccountList, GroupList, GroupDetail, ObtainJWTToken

urlpatterns = [
    path('token', ObtainJWTToken.as_view(), name='token_obtain'),
    path('users', UserList.as_view(), name='user_list'),
    path('accounts', AccountList.as_view(), name='account_list'),
    path('groups', GroupList.as_view(), name='group_list'),
    path('groups/<int:pk>', GroupDetail.as_view(), name='group_detail'),

]
