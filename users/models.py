from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    
    username = models.CharField(unique=True, max_length=255, default="")
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    location = models.CharField(max_length=255, default='YourDefaultValueHere')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='patient')


    def __str__(self):
        return self.username


# class Doctor(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=1)

# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     USER_TYPES = (
#         ('patient', 'Patient'),
#         ('doctor', 'Doctor'),
#         ('admin', 'Admin'),
#     )
#     user_type = models.CharField(max_length=10, choices=USER_TYPES, default='patient')
    
    # Add any other custom fields as needed



# class Doctor (models.Model):
#     username = models.CharField(
#         max_length=25, null=False, default='-', verbose_name='username')
#     password = models.CharField(
#         max_length=25, null=False, default='-', verbose_name='password')
#     first_name = models.CharField(
#         max_length=25, null=False, verbose_name='first_name')
#     last_name = models.CharField(
#         max_length=25, null=False, verbose_name='last_name')
#     phone = models.CharField(max_length=10, null=False,
#                              verbose_name='phone number')

#     def __str__(self):
#         return self.first_name

class Prediction(models.Model):
    age = models.CharField(max_length=5)
    height = models.IntegerField()
    weight = models.IntegerField()