from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Prediction,Result
from .forms import UserForm, UserRegisterForm
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A3

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
    actions = ['register_patient', 'register_doctor','export_selected_to_pdf']

    def register_patient(self, request, queryset):
        # Register selected users as patients
        queryset.update(user_type='patient')
    register_patient.short_description = "Register selected users as patients"

    def register_doctor(self, request, queryset):
        # Register selected users as doctors
        queryset.update(user_type='doctor')
    register_doctor.short_description = "Register selected users as doctors"
    

   


    def export_selected_to_pdf(self, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Prepare data for the table
        data = [['Username', 'Email', 'First Name', 'Last Name', 'Location', 'User Type']]
        users = queryset.values_list('username', 'email', 'first_name', 'last_name', 'location', 'user_type')
        for user in users:
            data.append(list(user))

        # Create the table
        table = Table(data)

        # Add a table style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])
        table.setStyle(style)

        # Add the table to the elements to be added to the PDF
        elements = []
        elements.append(table)

        # Build the PDF
        doc.build(elements)

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='users.pdf')

    export_selected_to_pdf.short_description = "Export selected users to PDF"

# Register the CustomUser model with the CustomUserAdmin class
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


    actions = ['export_selected_to_pdf']

    # other methods


    def export_selected_to_pdf(self, request, queryset):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(buffer, pagesize=A3)

        # Prepare data for the table
        data = [['D', 'P', 'A', 'H', 'W', 'G', 'SBP', 'DBP', 'C', 'G', 'S', 'A', 'A', 'P']]

        for result in queryset:
            doctor_name = result.doctor.full_name() if result.doctor else "Unknown"
            patient_name = result.patient.patient.full_name() if result.patient and result.patient.patient else "Unknown"
            data.append([
                doctor_name,
                patient_name,
                result.patient.age,
                result.patient.height,
                result.patient.weight,
                result.patient.gender,
                result.patient.systolic,
                result.patient.diastolic,
                result.patient.cholesterol,
                result.patient.glucose,
                result.patient.smoke,
                result.patient.alcohol,
                result.patient.active,
                result.prediction
            ])

        # Create the table with custom column widths
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 1.5*inch])

        # Add a table style with custom font size
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Increase font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ])
        table.setStyle(style)

        # Add a paragraph explaining the column names
        styles = getSampleStyleSheet()
        column_names = Paragraph('''
        <para align=center spaceb=3>
        <b>Column Names:</b> D: Doctor, P: Patient, A: Age, H: Height, W: Weight, G: Gender, SBP: Systolic BP, DBP: Diastolic BP, C: Cholesterol, G: Glucose, S: Smoker, A: Alcohol, A: Active, P: Prediction
        </para>''', styles['Normal'])
        # Add the paragraph to the elements to be added to the PDF
        elements = []
        elements.append(column_names)
        elements.append(table)

        # Build the PDF
        doc.build(elements)

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='results.pdf')

    export_selected_to_pdf.short_description = "Export selected results to PDF"
    
admin.site.register(Prediction, PredictionAdmin)
admin.site.register(Result, ResultAdmin)