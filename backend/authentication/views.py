from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from .views_base import CustomAPIView
from .models import User, Account, Group, Permission
from .serializers import UserSerializer, AccountSerializer, GroupSerializer, PermissionSerializer
from .permissions import IsAuthenticated, IsSuperuser, IsSameAccountOrIsSuperuser
from .jwt_authentication import CustomJWTAuthentication
from .decorators import get_and_check_object_permissions, check_permission, superuser_permission


class ObtainJWTToken(CustomAPIView):
    permission_classes = []

    @staticmethod
    def post(request: Request) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.authenticate(email=email, password=password)

        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'token': CustomJWTAuthentication.generate_jwt(user)}, status=status.HTTP_200_OK)


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

    @get_and_check_object_permissions(Account)
    @check_permission('view_account')
    def get(self, request: Request, account: Account) -> Response:
        serializer = AccountSerializer(instance=account)
        return Response(serializer.data)

    @get_and_check_object_permissions(Account)
    @check_permission('change_account')
    def put(self, request: Request, account: Account) -> Response:
        serializer = AccountSerializer(instance=account, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(Account)
    @check_permission('change_account')
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

    @superuser_permission()
    @get_and_check_object_permissions(Account)
    def delete(self, request: Request, account: Account) -> Response:
        account.delete()
        return Response({'success': 'Account deleted.'}, status=status.HTTP_204_NO_CONTENT)


class GroupList(CustomAPIView):
    permission_classes = [IsAuthenticated]

    @check_permission("view_group")
    def get(self, request: Request) -> Response:
        Groups = Group.objects.all()
        serializer = GroupSerializer(Groups, many=True)
        return Response(serializer.data)

    @check_permission("add_group")
    def post(self, request: Request) -> Response:
        serializer = GroupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupDetail(CustomAPIView):
    permission_classes = [IsAuthenticated, IsSameAccountOrIsSuperuser]

    @get_and_check_object_permissions(Group)
    @check_permission("view_group")
    def get(self, request: Request, group: Group) -> Response:
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    @get_and_check_object_permissions(Group)
    @check_permission("change_group")
    def put(self, request: Request, group: Group) -> Response:
        serializer = GroupSerializer(group, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(Group)
    @check_permission("change_group")
    def patch(self, request: Request, group: Group) -> Response:
        serializer = GroupSerializer(group, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(Group)
    @check_permission("delete_group")
    def delete(self, request: Request, group: Group) -> Response:
        group.delete()
        return Response({'success': 'Group deleted.'}, status=status.HTTP_204_NO_CONTENT)


class UserList(CustomAPIView):
    permission_classes = [IsAuthenticated]

    @check_permission("view_user")
    def get(self, request: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @check_permission("add_user")
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(CustomAPIView):
    permission_classes = [IsAuthenticated, IsSameAccountOrIsSuperuser]

    @get_and_check_object_permissions(User)
    @check_permission("view_user")
    def get(self, request: Request, user: User) -> Response:
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @get_and_check_object_permissions(User)
    @check_permission("change_user")
    def put(self, request: Request, user: User) -> Response:
        serializer = UserSerializer(instance=user, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(User)
    @check_permission("change_user")
    def patch(self, request: Request, user: User) -> Response:
        serializer = UserSerializer(
            instance=user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(User)
    @check_permission("delete_user")
    def delete(self, request: Request, user: User) -> Response:
        user.delete()
        return Response({'success': 'User deleted.'}, status=status.HTTP_204_NO_CONTENT)


class PermissionList(CustomAPIView):
    permission_classes = [IsAuthenticated]

    @check_permission("view_permission")
    def get(self, request: Request) -> Response:
        Permissions = Permission.objects.all()
        serializer = PermissionSerializer(Permissions, many=True)
        return Response(serializer.data)

    @superuser_permission()
    def post(request: Request) -> Response:
        serializer = PermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PermissionDetail(CustomAPIView):

    permission_classes = [IsAuthenticated]

    @get_and_check_object_permissions(Permission)
    @check_permission("view_permission")
    def get(self, request: Request, permission: Permission) -> Response:
        serializer = PermissionSerializer(permission)
        return Response(serializer.data)

    @get_and_check_object_permissions(Permission)
    @superuser_permission()
    def put(self, request: Request, permission: Permission) -> Response:
        serializer = PermissionSerializer(permission, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(Permission)
    @superuser_permission()
    def patch(self, request: Request, permission: Permission) -> Response:
        serializer = PermissionSerializer(
            permission, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(Permission)
    @superuser_permission()
    def delete(self, request: Request, permission: Permission) -> Permission:
        permission.delete()
        return Response({'success': 'Permission deleted.'}, status=status.HTTP_204_NO_CONTENT)
