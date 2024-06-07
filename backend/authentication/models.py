import bcrypt
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

class AccountManager(models.Manager):
    def create_account(self, name: str, **extra_fields)->'Account':
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
        
    def __str__(self)->str:
        return str({"content_type": "account", "id": self.id, "name": self.name})

class PermissionManager(models.Manager):
    def create_permission(self, name: str, **extra_fields)->'Permission':
        if not name: 
            raise ValueError('The name field must be set')
        name = name.strip()
        permission = self.model(name=name, **extra_fields)
        permission.save(using=self._db)
        return permission

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = PermissionManager()
    class Meta:
        db_table = 'authentication_permissions'
        
    def __str__(self)->str:
        return str({"content_type": "permission", "id": self.id, "name": self.name})
    
    pass

class UserManager(models.Manager):
    def create_user(self, email, password=None, **extra_fields)->'User':
        if not email: 
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields)->'User':
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users')
    permissions = models.ManyToManyField(Permission, related_name='users', db_table='authentication_user_permission', blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    
    def get_account(self) -> Account:
        return self.account

    def set_password(self, raw_password) -> 'User':
        self.password = self.hash_password(raw_password)
        return self

    def check_password(self, raw_password) -> bool:
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def hash_password(self, raw_password) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def clean(self) -> None:
        if not self.email:
            raise ValidationError(_('Email field cannot be empty'))
        if not self.password:
            raise ValidationError(_('Password field cannot be empty'))

    def save(self, *args, **kwargs) -> None:
        if self.pk is None and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'authentication_users'
        
    def __str__(self) -> str:
        return str({"content_type": "user", "id": self.id, "email": self.email})

class CustomAnonymousUser:
    is_authenticated = False

    def __str__(self):
        return 'AnonymousUser'
class GroupManager(models.Manager):
    def create_Group(self, name: str, **extra_fields)->'Group':
        if not name: 
            raise ValueError('The name field must be set')
        name = name.strip()
        Group = self.model(name=name, **extra_fields)
        Group.save(using=self._db)
        return Group

class Group(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(User, related_name='groups', db_table='authentication_group_user')
    permissions = models.ManyToManyField(Permission, related_name='groups',  db_table='authentication_group_permission')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GroupManager()
    
    class Meta:
        db_table = 'authentication_groups'
        
    def __str__(self)->str:
        return str({"content_type": "group", "id": self.id, "name": self.name})