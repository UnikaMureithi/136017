from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import PredictionForm
# from .models import Prediction
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    location = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'location', 'password1', 'password2']


# class UserPredictionForm(forms.ModelForm):
#     class Meta:
#         model = Prediction
#         fields = '__all__'

