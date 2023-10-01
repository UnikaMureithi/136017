from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Doctor (models.Model):
    first_name = models.CharField(
        max_length=25, null=False, verbose_name='first_name')
    last_name = models.CharField(
        max_length=25, null=False, verbose_name='last_name')
    phone = models.CharField(max_length=10, null=False,
                             verbose_name='phone number')

    def __str__(self):
        return self.first_name
