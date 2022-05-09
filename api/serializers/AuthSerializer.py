from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from api.models import Employee, Company
from rest_framework.authtoken.models import Token



# Employee Registration Serializer
#############################################################################################
class EmployeeCustomRegistrationSerializer(RegisterSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True,) #by default allow_null = False
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    def get_cleaned_data(self):
            data = super(EmployeeCustomRegistrationSerializer, self).get_cleaned_data()
            extra_data = {
                'first_name' : self.validated_data.get('first_name', ''),
                'last_name' : self.validated_data.get('last_name', ''),
            }
            data.update(extra_data)
            return data

    def save(self, request):
        user = super(EmployeeCustomRegistrationSerializer, self).save(request)
        user.is_employee = True
        user.save()
        employee = Employee(employee=user, first_name=self.cleaned_data.get('first_name'), 
                last_name=self.cleaned_data.get('last_name'))
        employee.save()
        return user



# Company Registration Serializer
#############################################################################################
class CompanyCustomRegistrationSerializer(RegisterSerializer):

    company = serializers.PrimaryKeyRelatedField(read_only=True,) #by default allow_null = False
    name = serializers.CharField(required=True)
    work_field = serializers.CharField(required=True)
    
    def get_cleaned_data(self):
            data = super(CompanyCustomRegistrationSerializer, self).get_cleaned_data()
            extra_data = {
                'name' : self.validated_data.get('name', ''),
                'work_field' : self.validated_data.get('work_field', ''),
            }
            data.update(extra_data)
            return data

    def save(self, request):
        user = super(CompanyCustomRegistrationSerializer, self).save(request)
        user.is_company = True
        user.save()
        company = Company(company=user, name=self.cleaned_data.get('name'), 
                work_field=self.cleaned_data.get('work_field'))
        company.save()
        return user        


