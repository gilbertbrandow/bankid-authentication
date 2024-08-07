import bcrypt
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from typing import Any, Optional, Set
from django.utils import timezone


class RefreshToken(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at if self.expires_at else False

    def __str__(self) -> str:
        return f"RefreshToken(user={self.user}, token={self.token})"

    class Meta:
        db_table: str = 'authentication_refresh_tokens'
        verbose_name: str = 'Refresh Token'
        verbose_name_plural: str = 'Refresh Tokens'


class AccountManager(models.Manager):
    def create_account(self, name: str, **extra_fields: Any) -> 'Account':
        if not name:
            raise ValueError('The name field must be set')
        name = name.strip()
        account = self.model(name=name, **extra_fields)
        account.save(using=self._db)
        return account


class Account(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AccountManager()

    class Meta:
        db_table = 'authentication_accounts'
        verbose_name: str = 'Account'
        verbose_name_plural: str = 'Accounts'

    def __str__(self) -> str:
        return str({"content_type": "account", "id": self.id, "name": self.name})


class BankIDAuthManager(models.Manager):
    pass


class BankIDAuthentication(models.Model):
    order_ref = models.CharField(max_length=255, unique=True, primary_key=True)
    auto_start_token = models.CharField(max_length=255)
    qr_start_token = models.CharField(max_length=255)
    qr_start_secret = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table: str = 'authentication_bankid'
        verbose_name: str = 'BankID Authentication'
        verbose_name_plural: str = 'BankID Authentications'

    def __str__(self) -> str:
        return self.order_ref


class PermissionManager(models.Manager):
    def create_permission(self, name: str, **extra_fields: Any) -> 'Permission':
        if not name:
            raise ValueError('The name field must be set')
        name = name.strip()
        permission = self.model(name=name, **extra_fields)
        permission.save(using=self._db)
        return permission


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PermissionManager()

    class Meta:
        db_table: str = 'authentication_permissions'
        verbose_name: str = 'Permission'
        verbose_name_plural: str = 'Permissions'

    def __str__(self) -> str:
        return str({"content_type": "permission", "id": self.id, "name": self.name})


class UserManager(models.Manager):
    def create_user(self, email: Optional[str], password: Optional[str] = None, **extra_fields: Any) -> 'User':
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: Optional[str], password: Optional[str] = None, **extra_fields: Any) -> 'User':
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def authenticate(self, email: Optional[str], password: Optional[str]) -> Optional['User']:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None


class User(models.Model):
    objects = UserManager()

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='users')
    """Should not be used for checking when permissions, needs to include all permissions in the users groups"""
    user_permissions = models.ManyToManyField(
        Permission, related_name='users', db_table='authentication_user_permission', blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    personal_number = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_authenticated = True

    @property
    def permissions(self) -> Set[Permission]:
        user_permissions = set(self.user_permissions.all())

        group_permissions = set()
        for group in self.groups.all():
            group_permissions.update(group.permissions.all())

        return user_permissions | group_permissions

    def get_account(self) -> Account:
        return self.account

    def set_password(self, raw_password: str) -> 'User':
        self.password = self.hash_password(raw_password)
        return self

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def hash_password(self, raw_password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def clean(self) -> None:
        if not self.email:
            raise ValidationError(_('Email field cannot be empty'))
        if not self.password:
            raise ValidationError(_('Password field cannot be empty'))

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.pk is None and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table: str = 'authentication_users'
        verbose_name: str = 'User'
        verbose_name_plural: str = 'Users'

    def __str__(self) -> str:
        return str({"content_type": "user", "id": self.id, "email": self.email})


class CustomAnonymousUser:
    is_authenticated = False

    def __str__(self) -> str:
        return 'AnonymousUser'


class GroupManager(models.Manager):
    def create_group(self, name: str, **extra_fields: Any) -> 'Group':
        if not name:
            raise ValueError('The name field must be set')
        name = name.strip()
        group = self.model(name=name, **extra_fields)
        group.save(using=self._db)
        return group


class Group(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(
        User, related_name='groups', db_table='authentication_group_user', blank=True)
    permissions = models.ManyToManyField(
        Permission, related_name='groups',  db_table='authentication_group_permission', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GroupManager()

    class Meta:
        db_table = 'authentication_groups'
        verbose_name: str = 'Group'
        verbose_name_plural: str = 'Groups'

    def __str__(self) -> str:
        return str({"content_type": "group", "id": self.id, "name": self.name})
