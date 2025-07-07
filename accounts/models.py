import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password, **extra_fields):
        """
          Create and save a SuperUser with the given email,first name , lastname and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('Username must be set'))
        if not password:
            raise ValueError(_('Password must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email,first name , lastname and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True, error_messages={
            'unique': _("A user with that username already exists."),
        },)
    email = models.CharField(max_length=200, unique=True, verbose_name='email address', error_messages={
            'unique': _("A user with that email already exists."),
        },)
    phone = PhoneNumberField(unique=True, error_messages={
            'unique': _("A user with that phone number already exists."),
        },)
    password = models.CharField(max_length=200)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # required for creating user
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return f'{self.username}'

