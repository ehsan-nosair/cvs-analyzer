from rest_framework import serializers

from api.models import EmployeeProfile, JobApplicant

class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'


class JobApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplicant
        fields = '__all__'