from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Prediction
from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'data-toggle': 'password',
        'id': 'password1',
        'onfocus': 'this.type="password"',
        }),
    )
    password2 = forms.CharField(
        label="Retype Password",
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'data-toggle': 'password',
        'id': 'password2',
        'onfocus': 'this.type="password"',
        }),
    )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, initial='patient', widget=forms.HiddenInput())
    # Set the initial value to 'patient' and hide the field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'location', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserPredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = '__all__'

