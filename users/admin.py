from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Prediction,Result
from .forms import UserForm, UserRegisterForm

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils import timezone

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def draw_table(pdf, headers, data, x, y):
    """
    Draw a table on the PDF.
    :param pdf: The PDF object.
    :param headers: List of table headers.
    :param data: List of lists containing table data.
    :param x: X-coordinate to start drawing the table.
    :param y: Y-coordinate to start drawing the table.
    """
    # Create a list to hold the data including headers
    table_data = [headers] + data

    # Set a fixed width for each column
    col_widths = [85, 140, 70, 70, 60, 70, 60, 60, 50, 50, 70, 70, 70, 70, 70, 80]

    # Create a Table object
    table = Table(table_data, colWidths=col_widths)

    # Apply styles to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Draw the table on the PDF
    table.wrapOn(pdf, pdf._pagesize[0] - 50, pdf._pagesize[1])
    table.drawOn(pdf, x, y)











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

    actions = ['register_patient', 'register_doctor', 'export_users_as_pdf']

    def export_users_as_pdf(self, request, queryset):
        # Generate and return the PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="selected_users_report.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Add a title to the PDF
        p.drawString(100, 800, "Selected Users Report")
        p.drawString(100, 780, f"Generated on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Export selected Users
        user_headers = ['Username', 'Email', 'First Name', 'Last Name', 'Location', 'User Type']
        user_data = [[user.username, user.email, user.first_name, user.last_name, user.location, user.user_type] for user in queryset]

        p.drawString(100, 750, "User Data:")
        draw_table(p, user_headers, user_data, 100, 730)

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        return response

    export_users_as_pdf.short_description = "Export selected users as PDF"

# Register the CustomUser model with the CustomUserAdmin class
# admin.site.register(CustomUser, CustomUserAdmin)

# Update the registration of CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)



class PredictionAdmin(admin.ModelAdmin):
    list_display = ['age', 'height', 'weight', 'gender', 'systolic', 'diastolic', 'cholesterol', 'glucose', 'smoke', 'alcohol', 'active']

class ResultAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'get_patient_age', 'get_patient_height', 'get_patient_weight', 'get_patient_gender', 'get_patient_systolic', 'get_patient_diastolic', 'get_patient_cholesterol', 'get_patient_glucose', 'get_patient_smoke', 'get_patient_alcohol', 'get_patient_active', 'prediction']

    def get_patient_age(self, obj):
        return obj.patient.age
    get_patient_age.short_description = 'Age'

    def get_patient_height(self, obj):
        return obj.patient.height
    get_patient_height.short_description = 'Height'

    def get_patient_weight(self, obj):
        return obj.patient.weight
    get_patient_weight.short_description = ' Weight'
    
    def get_patient_systolic(self, obj):
        return obj.patient.systolic
    get_patient_systolic.short_description = 'Systolic Blood Pressure'

    def get_patient_diastolic(self, obj):
        return obj.patient.diastolic
    get_patient_diastolic.short_description = 'Diastolic Blood Pressure'

    def get_patient_gender(self, obj):
        CHOICES = { 
            '1': 'male',
            '2': 'female',
        }
        return CHOICES.get(obj.patient.gender, 'Unknown')
    get_patient_gender.short_description = 'Gender'

    def get_patient_cholesterol(self, obj):
        CHOICES = {
            '1': 'Normal',
            '2': 'Above Normal',
            '3': 'Well Above Normal',
        }
        return CHOICES.get(str(obj.patient.cholesterol), 'Unknown')
    get_patient_cholesterol.short_description = 'Cholesterol'

   
    def get_patient_glucose(self, obj):
        CHOICES = {
            '1': 'Normal',
            '2': 'Above Normal',
            '3': 'Well Above Normal',
        }
        return CHOICES.get(str(obj.patient.glucose), 'Unknown')
    get_patient_glucose.short_description = 'Glucose'

    def get_patient_smoke(self, obj):
        CHOICES = {
            '0': 'Non-smoker',
            '1': 'Smoker',
        }
        return CHOICES.get(str(obj.patient.smoke), 'Unknown')
    get_patient_smoke.short_description = 'Smoking Status'

    def get_patient_alcohol(self, obj):
        CHOICES = {
            '0': 'no alcohol',
            '1': 'yes alcohol',
        }
        return CHOICES.get(str(obj.patient.alcohol), 'Unknown')
    get_patient_alcohol.short_description = 'Alcohol Intake'

    def get_patient_active(self, obj):
        CHOICES = {
            '0': 'not physically active',
            '1': 'physically active',
        }
        return CHOICES.get(str(obj.patient.active), 'Unknown')
    get_patient_active.short_description = 'Physical Activity'
    
    
admin.site.register(Prediction, PredictionAdmin)
admin.site.register(Result, ResultAdmin)