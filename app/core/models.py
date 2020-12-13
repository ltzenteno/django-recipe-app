from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """
    a Manager serves as a 'service' (coming from Java / Spring) for the model
    it has all the business logic validations and methods needed
    """

    def create_user(self, email, password=None, **extra_fields):
        """Creates, saves and returns a new user"""

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Creates, saves and returns a new super user"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
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
