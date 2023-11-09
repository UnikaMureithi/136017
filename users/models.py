from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
class PredictionResult(models.Model):
    prediction_id = models.AutoField(primary_key=True)
    prediction = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    
    username = models.CharField(unique=True, max_length=255, default="")
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    location = models.CharField(max_length=20, default='location')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='patient')


    def __str__(self):
        return self.username
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Prediction(models.Model):
#1: normal, 2: above normal, 3: well above normal
    cholesterol_level = (
        ('1', 'normal'),
        ('2', 'above normal'),
        ('3', 'well above normal'),

    )
    glucose_level = (
        ('1', 'normal'),
        ('2', 'above normal'),
        ('3', 'well above normal'),

    )
    smoking_status = (
        ('0', 'non-smoker'),
        ('1', 'smoker'),

    )
    alcohol_intake = (
        ('0', 'no alcohol'),
        ('1', 'yes alcohol'),

    )
    physical_activity = (
        ('0', 'not physically active'),
        ('1', 'physically active'),

    )
    gender = (
        ('1', 'male'),
        ('2', 'female'),

    )

    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()
    gender = models.CharField(max_length=10, choices=gender, default='male')
    systolic_blood_pressure = models.FloatField(default=0)
    diastolic_bp = models.FloatField(default=0, null=True)
    cholesterol = models.CharField(max_length=6, choices=cholesterol_level, default='normal')
    glucose = models.CharField(max_length=25, choices=glucose_level, default='normal')
    smoking_status = models.CharField(max_length=25, choices=smoking_status, default='non-smoker')
    alcohol_intake = models.CharField(max_length=25, choices=alcohol_intake, default='no_alcohol')
    physical_activity = models.CharField(max_length=25, choices=physical_activity, default='no')
