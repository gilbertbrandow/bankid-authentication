from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from .views_base import CustomAPIView
from .models import User, Account, Group, Permission
from .serializers import UserSerializer, AccountSerializer, GroupSerializer, PermissionSerializer
from .permissions import IsAuthenticated, IsSuperuser, IsSameAccountOrIsSuperuser, HasPermission
from .jwt_authentication import CustomJWTAuthentication
from .decorators import get_and_check_object_permissions


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
    permission_classes = [IsSuperuser]

    @staticmethod
    def get(request: Request) -> Response:
        Accounts = Account.objects.all()
        serializer = AccountSerializer(Accounts, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request: Request) -> Response:
        serializer = AccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountDetail(CustomAPIView):
    permission_classes = [IsSameAccountOrIsSuperuser]

    @get_and_check_object_permissions(Account)
    def get(self, request: Request, account: Account) -> Response:
        serializer = AccountSerializer(instance=account)
        return Response(serializer.data)

    @get_and_check_object_permissions(Account)
    def put(self, request: Request, account: Account) -> Response:
        serializer = AccountSerializer(instance=account, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @get_and_check_object_permissions(Account)
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

    @get_and_check_object_permissions(Account)
    def delete(self, request: Request, account: Account) -> Response:
        account.delete()
        return Response({'success': 'Account deleted.'}, status=status.HTTP_204_NO_CONTENT)


class GroupList(CustomAPIView):

    def get_permissions(self):
        permissions = [IsAuthenticated()]

        if self.request.method == 'GET':
            permissions.append(HasPermission(permission_codename='view_group'))
        elif self.request.method == 'POST':
            permissions.append(HasPermission(permission_codename='add_group'))
        return permissions

    @staticmethod
    def get(request: Request) -> Response:
        Groups = Group.objects.all()
        serializer = GroupSerializer(Groups, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request: Request) -> Response:
        serializer = GroupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupDetail(CustomAPIView):
    def get_permissions(self):
        permissions = [IsSameAccountOrIsSuperuser()]

        if self.request.method == 'GET':
            permissions.append(HasPermission(permission_codename='view_group'))
        elif self.request.method in ['PUT', 'PATCH']:
            permissions.append(HasPermission(
                permission_codename='change_group'))
        elif self.request.method == 'DELETE':
            permissions.append(HasPermission(
                permission_codename='delete_group'))

        return permissions

    @staticmethod
    def get_object(pk: int) -> Group | None:
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return None

    def get(self, request: Request, pk: int) -> Group:
        group = self.get_object(pk)

        if group is None:
            return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, group)

        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Group:
        group = self.get_object(pk)

        if group is None:
            return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, group)

        serializer = GroupSerializer(group, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Group:
        group = self.get_object(pk)

        if group is None:
            return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, group)

        serializer = GroupSerializer(group, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, pk: int) -> Group:
        group = self.get_object(pk)

        if group is None:
            return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, group)

        group.delete()
        return Response({'success': 'Group deleted.'}, status=status.HTTP_204_NO_CONTENT)


class UserList(CustomAPIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(CustomAPIView):
    permission_classes = [IsSameAccountOrIsSuperuser]

    @staticmethod
    def get_object(pk: int) -> User | None:
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request: Request, pk: int) -> User:
        user = self.get_object(pk)

        if user is None:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> User:
        user = self.get_object(pk)

        if user is None:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> User:
        user = self.get_object(pk)

        if user is None:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, pk: int) -> User:
        user = self.get_object(pk)

        if user is None:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)

        user.delete()
        return Response({'success': 'User deleted.'}, status=status.HTTP_204_NO_CONTENT)


class PermissionList(CustomAPIView):

    def get_permissions(self) -> list:
        if self.request.method == 'POST':
            return [IsSuperuser]
        return [IsAuthenticated]

    @staticmethod
    def get(request: Request) -> Response:
        Permissions = Permission.objects.all()
        serializer = PermissionSerializer(Permissions, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request: Request) -> Response:
        serializer = PermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PermissionDetail(CustomAPIView):

    def get_permissions(self) -> list:
        if self.request.method == 'GET':
            return [IsAuthenticated]
        return [IsSuperuser]

    @staticmethod
    def get_object(pk: int) -> Permission | None:
        try:
            return Permission.objects.get(pk=pk)
        except Permission.DoesNotExist:
            return None

    def get(self, request: Request, pk: int) -> Permission:
        permission = self.get_object(pk)

        if permission is None:
            return Response({'detail': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermissionSerializer(permission)
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Permission:
        permission = self.get_object(pk)

        if permission is None:
            return Response({'detail': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermissionSerializer(permission, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Permission:
        permission = self.get_object(pk)

        if permission is None:
            return Response({'detail': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermissionSerializer(
            permission, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, pk: int) -> Permission:
        permission = self.get_object(pk)

        if permission is None:
            return Response({'detail': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)

        permission.delete()
        return Response({'success': 'Permission deleted.'}, status=status.HTTP_204_NO_CONTENT)
