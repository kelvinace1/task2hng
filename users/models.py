from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, PermissionsMixin, Permission
from django.db import models
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None, phone=None):
        if not email:
            raise ValueError('User must have an email address')
        if not firstName:
            raise ValueError('User must have a first name')
        if not lastName:
            raise ValueError('User must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, password=None):
        user = self.create_user(
            email=email,
            firstName=firstName,
            lastName=lastName,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    firstName = models.CharField(max_length=30, null=False)
    lastName = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        Group,
        related_name='users_groups',  
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='users_permissions',  
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email