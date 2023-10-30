from django.contrib import admin
from users import models
# Register your models here.

# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_patient', 'is_doctor')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_patient', 'is_doctor')

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ('username', 'email', 'is_patient', 'is_doctor')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_patient', 'is_doctor')
    list_filter = ('is_patient', 'is_doctor')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Custom Fields', {'fields': ('is_patient', 'is_doctor')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)


# admin.site.register(models.Doctor)
