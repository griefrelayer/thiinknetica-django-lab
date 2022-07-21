from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Custom user model with extra fields"""
    phone_number = PhoneNumberField(null=True)

    class Meta:
        db_table = 'auth_user'


# Create your models here.
