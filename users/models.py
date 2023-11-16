from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

  
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


    def _str_(self):
        return self.username
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Prediction(models.Model):
    # Choices for categorical fields
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

    prediction_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_predictions')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_predictions')
    name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()
    gender = models.CharField(max_length=10, choices=gender, default='male')
    systolic = models.FloatField(default=0)
    diastolic = models.FloatField(null=True)
    cholesterol = models.CharField(max_length=6, choices=cholesterol_level, default='normal')
    glucose = models.CharField(max_length=25, choices=glucose_level, default='normal')
    smoke = models.CharField(max_length=25, choices=smoking_status, default='non-smoker')
    alcohol = models.CharField(max_length=25, choices=alcohol_intake, default='no_alcohol')
    active = models.CharField(max_length=25, choices=physical_activity, default='no')
    
    
    
    
       

    def _str_(self):
        return f'{self.patient.first_name} {self.patient.last_name}'
    
    def clean(self):
        if self.age < 0:
            raise ValidationError("Age cannot be negative.")
        if not (50 < self.height < 300):
            raise ValidationError("Height must be between 50 and 300.")
        if not (2 < self.weight < 500):
            raise ValidationError("Weight must be between 2 and 500.")
    


User = get_user_model() 

class Result(models.Model):
    prediction_id = models.AutoField(primary_key=True)
    prediction = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # ForeignKey for the logged-in user
    patient = models.ForeignKey(Prediction, on_delete=models.CASCADE, null=True) 
    
    def save(self, *args, **kwargs):
        # Convert the prediction to a string before saving
        self.prediction = str(self.prediction)
        super().save(*args, **kwargs)

    # def _str_(self):
    #     doctor_name = self.doctor.full_name() if self.doctor else "Unknown"
    #     patient_name = self.patient.patient.full_name() if self.patient and self.patient.patient else "Unknown"
    #     return f"Prediction ID: {self.prediction_id}, Doctor: {doctor_name}, Patient: {patient_name}, Age: {self.patient.age}, Height: {self.patient.height}, Weight: {self.patient.weight}, Gender: {self.patient.gender}, Systolic BP: {self.patient.systolic}, Diastolic BP: {self.patient.diastolic}, Cholesterol: {self.patient.cholesterol}, Glucose: {self.patient.glucose}, Smoking Status: {self.patient.smoke}, Alcohol Intake: {self.patient.active}, Physical Activity: {self.patient.active}, Prediction: {self.prediction}"

def __str__(self):
    doctor_name = self.doctor.full_name() if self.doctor else "Unknown"

    patient_name = "Unknown"
    if self.patient_id:
        try:
            patient_name = CustomUser.objects.get(id=self.patient_id).full_name()
        except CustomUser.DoesNotExist:
            pass

    return f"Prediction ID: {self.prediction_id}, Doctor: {doctor_name}, Patient: {patient_name}, Prediction: {self.prediction}"
