# Generated by Django 4.2.5 on 2023-11-08 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_alter_prediction_diastolic_blood_pressure_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prediction',
            name='diastolic_blood_pressure',
        ),
    ]
