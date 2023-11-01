# Generated by Django 4.2.5 on 2023-10-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_doctor_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(max_length=5)),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='username',
            field=models.CharField(default='0', max_length=25, verbose_name='username'),
        ),
    ]