# Generated by Django 4.2.5 on 2023-11-08 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_prediction_diastolic_blood_pressure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='diastolic_blood_pressure',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
