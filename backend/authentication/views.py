import requests
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from .views_base import CustomAPIView
from .models import User, Account, Group, Permission
from .serializers import UserSerializer, AccountSerializer, GroupSerializer, PermissionSerializer
from .permissions import IsAuthenticated, IsSuperuser, IsSameAccountOrIsSuperuser
from .decorators import get_and_check_object_permissions, check_permission, check_superuser_permission
class AccountList(CustomAPIView):
    permission_classes = [IsAuthenticated, IsSuperuser]

    @staticmethod
    def get(request: Request) -> Response:
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request: Request) -> Response:
        serializer = AccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountDetail(CustomAPIView):
    permission_classes = [IsAuthenticated, IsSameAccountOrIsSuperuser]

    @get_and_check_object_permissions(model=Account)
    @check_permission(permission_codename='view_account')
    def get(self, request: Request, account: Account) -> Response:
        serializer = AccountSerializer(instance=account)
        return Response(serializer.data)

    @get_and_check_object_permissions(model=Account)
    @check_permission(permission_codename='change_account')
    def put(self, request: Request, account: Account) -> Response:
        serializer = AccountSerializer(instance=account, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(model=Account)
    @check_permission(permission_codename='change_account')
    def patch(self, request: Request, account: Account) -> Response:
        serializer = AccountSerializer(
            instance=account,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @check_superuser_permission()
    @get_and_check_object_permissions(model=Account)
    def delete(self, request: Request, account: Account) -> Response:
        account.delete()
        return Response({'success': 'Account deleted.'}, status=status.HTTP_204_NO_CONTENT)


class GroupList(CustomAPIView):
    permission_classes = [IsAuthenticated]

    @check_permission(permission_codename="view_group")
    def get(self, request: Request) -> Response:
        Groups = Group.objects.all()
        serializer = GroupSerializer(Groups, many=True)
        return Response(serializer.data)

    @check_permission(permission_codename="add_group")
    def post(self, request: Request) -> Response:
        serializer = GroupSerializer(
            data=request.data,
            context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupDetail(CustomAPIView):
    permission_classes = [IsAuthenticated, IsSameAccountOrIsSuperuser]

    @get_and_check_object_permissions(model=Group)
    @check_permission(permission_codename="view_group")
    def get(self, request: Request, group: Group) -> Response:
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    @get_and_check_object_permissions(model=Group)
    @check_permission(permission_codename="change_group")
    def put(self, request: Request, group: Group) -> Response:
        serializer = GroupSerializer(
            instance=group,
            data=request.data,
            context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(model=Group)
    @check_permission(permission_codename="change_group")
    def patch(self, request: Request, group: Group) -> Response:
        serializer = GroupSerializer(
            instance=group,
            data=request.data,
            partial=True,
            context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(model=Group)
    @check_permission(permission_codename="delete_group")
    def delete(self, request: Request, group: Group) -> Response:
        group.delete()
        return Response({'success': 'Group deleted.'}, status=status.HTTP_204_NO_CONTENT)


class UserList(CustomAPIView):
    permission_classes = [IsAuthenticated]

    @check_permission(permission_codename="view_user")
    def get(self, request: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @check_permission(permission_codename="add_user")
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(
            data=request.data,
            context={'request': request})

        if serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(CustomAPIView):
    permission_classes = [IsAuthenticated, IsSameAccountOrIsSuperuser]

    @get_and_check_object_permissions(model=User)
    @check_permission(permission_codename="view_user")
    def get(self, request: Request, user: User) -> Response:
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @get_and_check_object_permissions(model=User)
    @check_permission(permission_codename="change_user")
    def put(self, request: Request, user: User) -> Response:
        serializer = UserSerializer(
            instance=user,
            data=request.data,
            context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(model=User)
    @check_permission(permission_codename="change_user")
    def patch(self, request: Request, user: User) -> Response:
        serializer = UserSerializer(
            instance=user,
            data=request.data,
            partial=True,
            context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(model=User)
    @check_permission(permission_codename="delete_user")
    def delete(self, request: Request, user: User) -> Response:
        user.delete()
        return Response({'success': 'User deleted.'}, status=status.HTTP_204_NO_CONTENT)


class PermissionList(CustomAPIView):
    permission_classes = [IsAuthenticated]

    @check_permission(permission_codename="view_permission")
    def get(self, request: Request) -> Response:
        Permissions = Permission.objects.all()
        serializer = PermissionSerializer(Permissions, many=True)
        return Response(serializer.data)

    @check_superuser_permission()
    def post(request: Request) -> Response:
        serializer = PermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PermissionDetail(CustomAPIView):

    permission_classes = [IsAuthenticated]

    @get_and_check_object_permissions(model=Permission)
    @check_permission(permission_codename="view_permission")
    def get(self, request: Request, permission: Permission) -> Response:
        serializer = PermissionSerializer(permission)
        return Response(serializer.data)

    @get_and_check_object_permissions(model=Permission)
    @check_superuser_permission()
    def put(self, request: Request, permission: Permission) -> Response:
        serializer = PermissionSerializer(permission, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(model=Permission)
    @check_superuser_permission()
    def patch(self, request: Request, permission: Permission) -> Response:
        serializer = PermissionSerializer(
            permission, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(model=Permission)
    @check_superuser_permission()
    def delete(self, request: Request, permission: Permission) -> Response:
        permission.delete()
        return Response({'success': 'Permission deleted.'}, status=status.HTTP_204_NO_CONTENT)
