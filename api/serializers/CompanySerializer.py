from rest_framework import serializers

from api.models import Job, JobApplicant, JobResult

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplicant
        fields = '__all__'


class JobResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = '__all__'