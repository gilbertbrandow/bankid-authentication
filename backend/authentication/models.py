import bcrypt
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class AccountManager(models.Manager):
    def create_account(self, title: str, **extra_fields)->'Account':
        if not title: 
            raise ValueError('The title field must be set')
        title = title.strip()
        account = self.model(title=title, **extra_fields)
        account.save(using=self._db)
        return account

class Account(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AccountManager()
    
    def __str__(self)->str:
        return str({"type": "account", "id": self.id, "title": self.title})


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
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    
    def get_account(self)->Account:
        return self.account

    def set_password(self, raw_password)->'User':
        self.password = self.hash_password(raw_password)
        return self

    def check_password(self, raw_password)->bool:
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def hash_password(self, raw_password)->str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def clean(self)->None:
        if not self.email:
            raise ValidationError(_('Email field cannot be empty'))
        if not self.password:
            raise ValidationError(_('Password field cannot be empty'))

    def save(self, *args, **kwargs)->None:
        if self.pk is None and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self)->str:
        return str({"type": "user", "id": self.id, "email": self.email})


class GroupManager(models.Manager):
    def create_Group(self, title: str, **extra_fields)->'Group':
        if not title: 
            raise ValueError('The title field must be set')
        title = title.strip()
        Group = self.model(title=title, **extra_fields)
        Group.save(using=self._db)
        return Group

class Group(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users')
    title = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(User, related_name='groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GroupManager()
    
    def __str__(self)->str:
        return str({"type": "Group", "id": self.id, "title": self.title})