# Generated by Django 4.2.5 on 2023-11-16 15:55

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(default='', max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('location', models.CharField(default='location', max_length=20)),
                ('user_type', models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')], default='patient', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('prediction_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('age', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.FloatField()),
                ('gender', models.CharField(choices=[('1', 'male'), ('2', 'female')], default='male', max_length=10)),
                ('systolic', models.FloatField(default=0)),
                ('diastolic', models.FloatField(null=True)),
                ('cholesterol', models.CharField(choices=[('1', 'normal'), ('2', 'above normal'), ('3', 'well above normal')], default='normal', max_length=6)),
                ('glucose', models.CharField(choices=[('1', 'normal'), ('2', 'above normal'), ('3', 'well above normal')], default='normal', max_length=25)),
                ('smoke', models.CharField(choices=[('0', 'non-smoker'), ('1', 'smoker')], default='non-smoker', max_length=25)),
                ('alcohol', models.CharField(choices=[('0', 'no alcohol'), ('1', 'yes alcohol')], default='no_alcohol', max_length=25)),
                ('active', models.CharField(choices=[('0', 'not physically active'), ('1', 'physically active')], default='no', max_length=25)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_predictions', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_predictions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('prediction_id', models.AutoField(primary_key=True, serialize=False)),
                ('prediction', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.prediction')),
            ],
        ),
    ]
