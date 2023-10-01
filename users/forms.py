from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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
