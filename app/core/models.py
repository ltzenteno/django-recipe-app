from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates, saves and returns a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(
        max_length=255,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    objects = UserManager()

    # overriding the default USERNAME_FIELD from the PermissionsMixin to be the `email` instead of the `username` # noqa: E501
    USERNAME_FIELD = 'email'
