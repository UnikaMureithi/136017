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
        user = super(UserRegisterForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserPredictionForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
    queryset=CustomUser.objects.filter(user_type='patient'),
    to_field_name='id',  # Specify the field to use for values
    label='Select a Patient',
    empty_label='Select a Patient',
    )
    class Meta:
        model = Prediction
        fields = '__all__'

    # Specify the order of fields in the form
    fields = ['patient', 'age', 'height', 'weight', 'gender', 'systolic_blood_pressure', 'diastolic_bp', 'cholesterol', 'glucose', 'smoking_status', 'alcohol_intake', 'physical_activity']