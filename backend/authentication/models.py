import bcrypt
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=128)

    objects = UserManager()

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

    def __str__(self):
        return self.email