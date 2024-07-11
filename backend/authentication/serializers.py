from typing import Any, Dict
from rest_framework import serializers
from .models import RefreshToken, Account, Group, Permission, User
from rest_framework.request import Request


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

    def create(self, validated_data: Dict[str, Any]) -> Group:
        request: Request = self.context.get('request')
        if request and not request.user.is_superuser:
            validated_data['account'] = request.user.account
        return super().create(validated_data)

    def update(self, instance: Group, validated_data: Dict[str, Any]) -> Group:
        request: Request = self.context.get('request')
        if request and not request.user.is_superuser:
            validated_data['account'] = request.user.account
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser',
            'created_at', 'updated_at', 'account', 'user_permissions', 'groups'
        ]

    def create(self, validated_data: Dict[str, Any]) -> User:
        request: Request = self.context.get('request')
        if request and not request.user.is_superuser:
            validated_data['account'] = request.user.account
        return super().create(validated_data)

    def update(self, instance: User, validated_data: Dict[str, Any]) -> User:
        request: Request = self.context.get('request')
        if request and not request.user.is_superuser:
            validated_data['account'] = request.user.account
        return super().update(instance, validated_data)


class RefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshToken
        fields = ['user', 'token', 'created_at', 'expires_at']
        read_only_fields = ['created_at', 'expires_at']