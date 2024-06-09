from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Account, Group
from .serializers import UserSerializer, AccountSerializer, GroupSerializer
from rest_framework.permissions import IsAuthenticated
from .jwt_authentication import generate_jwt
class ObtainJWTToken(APIView):
    permission_classes = []
    
    def post(self, request: HttpRequest) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.authenticate(email=email, password=password)
        
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'token': generate_jwt(user)}, status=status.HTTP_200_OK)
        
class AccountList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        Accounts = Account.objects.all()
        serializer = AccountSerializer(Accounts, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        serializer = AccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AccountDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk: int) -> Account | None:
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return None

    def get(self, request: HttpRequest, pk: int) -> Account:
        account = self.get_object(pk)
        
        if account is None:
            return Response({'detail': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request: HttpRequest, pk: int) -> Account:
        account = self.get_object(pk)
        
        if account is None:
            return Response({'detail': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AccountSerializer(account, data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)

    def patch(self, request: HttpRequest, pk: int) -> Account:
        account = self.get_object(pk)
        
        if account is None:
            return Response({'detail': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AccountSerializer(account, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)
        
    def delete(self, request: HttpRequest, pk: int) -> Account:
        account = self.get_object(pk)
        
        if account is None:
            return Response({'detail': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        
        account.delete()
        return Response({'success': 'Account deleted.'}, status=status.HTTP_204_NO_CONTENT)


class GroupList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request: HttpRequest) -> Response:
        Groups = Group.objects.all()
        serializer = GroupSerializer(Groups, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        serializer = GroupSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class GroupDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk: int) -> Group | None:
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return None

    def get(self, request: HttpRequest, pk: int) -> Group:
        group = self.get_object(pk)
        
        if group is None:
            return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request: HttpRequest, pk: int) -> Group:
        group = self.get_object(pk)
        
        if group is None:
            return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GroupSerializer(group, data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)

    def patch(self, request: HttpRequest, pk: int) -> Group:
        group = self.get_object(pk)
        
        if group is None:
            return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GroupSerializer(group, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)
        
    def delete(self, request: HttpRequest, pk: int) -> Group:
        group = self.get_object(pk)
        
        if group is None:
            return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        
        group.delete()
        return Response({'success': 'Group deleted.'}, status=status.HTTP_204_NO_CONTENT)
    
class UserList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request: HttpRequest) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk: int) -> User | None:
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request: HttpRequest, pk: int) -> User:
        user = self.get_object(pk)
        
        if user is None:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request: HttpRequest, pk: int) -> User:
        user = self.get_object(pk)
        
        if user is None:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)

    def patch(self, request: HttpRequest, pk: int) -> User:
        user = self.get_object(pk)
        
        if user is None:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)
        
    def delete(self, request: HttpRequest, pk: int) -> User:
        user = self.get_object(pk)
        
        if user is None:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response({'success': 'User deleted.'}, status=status.HTTP_204_NO_CONTENT)
    