from rest_framework import serializers
from .models import Account, Group, Permission, User

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True) 

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser',
            'created_at', 'updated_at', 'account', 'user_permissions', 'groups'
        ]