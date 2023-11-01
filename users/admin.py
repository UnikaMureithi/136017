from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import UserForm, UserRegisterForm

class CustomUserAdmin(UserAdmin):
    add_form = UserForm  # Use the UserForm for adding users
    form = UserRegisterForm  # Use the UserRegisterForm for updating users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'location', 'password1', 'password2', 'user_type')
        }),
    )

    # Customize the list of columns to be displayed in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'location', 'user_type')

    # Allow admin to register users for both user types
    actions = ['register_patient', 'register_doctor']

    def register_patient(self, request, queryset):
        # Register selected users as patients
        queryset.update(user_type='patient')
    register_patient.short_description = "Register selected users as patients"

    def register_doctor(self, request, queryset):
        # Register selected users as doctors
        queryset.update(user_type='doctor')
    register_doctor.short_description = "Register selected users as doctors"

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
