"""
URL configuration for authentication.

"""

from django.urls import path
from .views import AccountList, AccountDetail, GroupList, GroupDetail, UserList, UserDetail, PermissionList, PermissionDetail, ObtainJWTToken, bankid_initiate_authentication, generate_qr_code, poll_authentication_status

urlpatterns = [
    path('token/', ObtainJWTToken.as_view(), name='token_obtain'),
    
    # Authentication app CRUD
    path('accounts/', AccountList.as_view(), name='account_list'),
    path('accounts/<int:pk>/', AccountDetail.as_view(), name='account_detail'),
    path('groups/', GroupList.as_view(), name='group_list'),
    path('groups/<int:pk>/', GroupDetail.as_view(), name='group_detail'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('permissions/', PermissionList.as_view(), name='permission_list'),
    path('permissions/<int:pk>/', PermissionDetail.as_view(), name='permission_detail'),
    
    # BankID authentication
    path('bankid/initiate/', bankid_initiate_authentication, name='bankid_initiate'),
    path('bankid/qr/<str:order_ref>/', generate_qr_code, name='bankid_qr_code'),
    path('bankid/poll/<str:order_ref>/', poll_authentication_status, name='bankid_poll'),
]
