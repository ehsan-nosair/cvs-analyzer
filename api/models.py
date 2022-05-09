from enum import unique
from tkinter import CASCADE
from wsgiref.validate import validator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField

from api.helpers import RandomFileName
# Create your models here.


class User(AbstractUser):
  #Boolean fields to select the type of account.
  is_employee = models.BooleanField(default=False)
  is_company = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)


# user type 1 Employee
#############################################################################################
class Employee(models.Model):
    employee = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.employee.username



# user type 2 Company
#############################################################################################
class Company(models.Model):
    company = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    work_field = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.company.username


# user type 3 Admin
#############################################################################################
class Admin(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    # def __str__(self):
    #     return self.admin.username


# employee profile
#############################################################################################
class EmployeeProfile(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, blank=True)
    image = models.ImageField('Image',upload_to=RandomFileName('images/profile'), validators=[FileExtensionValidator(allowed_extensions=['png','jpg','webp','svg'])] , blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True, unique=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    previous_works = models.TextField(blank=True, null=True)
    languages = models.TextField(blank=True, null=True)
    softskills = models.TextField(blank=True, null=True)
    cv = models.FileField(upload_to=RandomFileName('files/employees/cvs'), validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)


# jobs
#############################################################################################
class Job(models.Model):
    TYPES = (
        ('with cvs' , 'with cvs'),
        ('without cvs' , 'without cvs')
    )
    STATUS = (
        ('ongoing' , 'ongoing'),
        ('finished' , 'finished')
    )

    company = models.ForeignKey(Company, on_delete= models.CASCADE)

    subject = models.CharField(max_length=200, null=False)
    type = status = models.CharField(max_length=200, null=False, choices=TYPES)
    cvs = models.FileField(upload_to=RandomFileName('files/companies/cvs'), validators=[FileExtensionValidator(allowed_extensions=['zip'])], blank=True, null=True)
    required_skills = models.TextField(blank=True, null=True)
    required_work_experience = models.TextField(blank=True, null=True)
    required_soft_skills = models.TextField(blank=True, null=True)
    required_languages = models.TextField(blank=True, null=True)
    expire_time = models.DateField(null = False)
    status = models.CharField(max_length=200, null=True, choices=STATUS)


# job_applicants
#############################################################################################
class JobApplicant(models.Model):
    job = models.ForeignKey(Job, on_delete= models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete= models.CASCADE)
    email = models.EmailField(max_length=254)
    score = models.IntegerField(null = True)


# job results
#############################################################################################
class JobResult(models.Model):
    job = models.ForeignKey(Job, on_delete= models.CASCADE)
    cvs_score = models.JSONField()

    