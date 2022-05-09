# Generated by Django 3.1.2 on 2022-04-26 10:49

import api.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/profile/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'webp', 'svg'])])),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('skills', models.TextField(blank=True, null=True)),
                ('previous_works', models.TextField(blank=True, null=True)),
                ('languages', models.TextField(blank=True, null=True)),
                ('softskills', models.TextField(blank=True, null=True)),
                ('cv', models.FileField(blank=True, null=True, upload_to='files/cvs/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('employee', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.employee')),
            ],
        ),
    ]