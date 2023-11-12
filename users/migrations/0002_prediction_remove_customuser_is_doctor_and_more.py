# Generated by Django 4.2.5 on 2023-11-11 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.FloatField()),
                ('gender', models.CharField(choices=[('1', 'male'), ('2', 'female')], default='male', max_length=10)),
                ('systolic_blood_pressure', models.FloatField(default=0)),
                ('diastolic_bp', models.FloatField(null=True)),
                ('cholesterol', models.CharField(choices=[('1', 'normal'), ('2', 'above normal'), ('3', 'well above normal')], default='normal', max_length=6)),
                ('glucose', models.CharField(choices=[('1', 'normal'), ('2', 'above normal'), ('3', 'well above normal')], default='normal', max_length=25)),
                ('smoking_status', models.CharField(choices=[('0', 'non-smoker'), ('1', 'smoker')], default='non-smoker', max_length=25)),
                ('alcohol_intake', models.CharField(choices=[('0', 'no alcohol'), ('1', 'yes alcohol')], default='no_alcohol', max_length=25)),
                ('physical_activity', models.CharField(choices=[('0', 'not physically active'), ('1', 'physically active')], default='no', max_length=25)),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_doctor',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_patient',
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')], default='patient', max_length=10),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='location',
            field=models.CharField(default='location', max_length=20),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('prediction_id', models.AutoField(primary_key=True, serialize=False)),
                ('prediction', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.prediction')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
