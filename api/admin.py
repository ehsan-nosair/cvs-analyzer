from django.contrib import admin
from api.models import Employee, Company, User, EmployeeProfile, Job

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(EmployeeProfile)
admin.site.register(Job)