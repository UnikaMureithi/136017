# Generated by Django 4.2.5 on 2023-11-08 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_prediction_diastolic_blood_pressure'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionResult',
            fields=[
                ('prediction_id', models.AutoField(primary_key=True, serialize=False)),
                ('prediction', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
