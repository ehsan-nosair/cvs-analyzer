from random import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.decorators import required_roles
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from api.models import Employee, EmployeeProfile, Job, JobApplicant, JobResult
from api.serializers.CompanySerializer import JobApplicantSerializer, JobResultsSerializer, JobSerializer
from api.serializers.EmployeeSerializer import EmployeeProfileSerializer


##### Job Functions
#####################################################################################


# 1
# get all related jobs
#
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['company'])
def job_list(request):
    data = Job.objects.all()
    serializer = JobSerializer(data, many = True)
    return Response(serializer.data)


# 2
# show job details
#
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['company', 'employee'])
def job_details(request, id):
    try:
        data = Job.objects.get(id = id)
        serializer = JobSerializer(data)

        if(data.type == 'without cvs'):
            results = JobApplicant.objects.filter(job_id = id).order_by('-score')
            result_serializer = JobApplicantSerializer(results, many=True).data
        elif(data.type == 'with cvs'):
            results = JobResult.objects.get(job_id = id)
            result_serializer = JobResultsSerializer(results).data

        response_data = {
            "job": serializer.data,
            "results": result_serializer
        }
        return Response(response_data, status.HTTP_200_OK)
    except Job.DoesNotExist:
        response_data = {
            "message": "Job Not Found"
        }
        return Response(response_data, status.HTTP_404_NOT_FOUND)


# 3
# create new job
#
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['company'])
def job_create(request):
    serializer = JobSerializer(data = request.data)
    if(serializer.is_valid()):
        data = Job.objects.create(
            company = serializer.validated_data.get('company'),
            subject = serializer.validated_data.get('subject'),
            type = serializer.validated_data.get('type'),
            cvs = serializer.validated_data.get('cvs'),
            required_skills = serializer.validated_data.get('required_skills'),
            required_work_experience = serializer.validated_data.get('required_work_experience'),
            required_soft_skills = serializer.validated_data.get('required_soft_skills'),
            required_languages = serializer.validated_data.get('required_languages'),
            expire_time = serializer.validated_data.get('expire_time'),
            status = 'ongoing'
        )

        if(serializer.validated_data.get('type') == 'with cvs'):
            # analize cvs py AI (in queue)
            results = []
            for i in range(5):
                cv = {
                    'cv_number': i,
                    'cv_score': randint(1, 100) 
                }
                results.append(cv)
            JobResult.objects.create(
                cvs_score = results,
                job_id = data.id
            )

        response_data = JobSerializer(data).data
        return Response(response_data, status.HTTP_200_OK)
    else:
        response_data = {
            'message': 'validation error',
            'data': serializer.errors
        }    
        return Response(response_data, status.HTTP_422_UNPROCESSABLE_ENTITY)


# 4
# update job
#
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['company'])
def job_update(request, id):
    serializer = JobSerializer(data = request.data)
    if(serializer.is_valid()):
        obj = Job.objects.get(id = id)
        obj.subject = serializer.validated_data.get('subject')
        obj.type = serializer.validated_data.get('type')
        obj.cvs = serializer.validated_data.get('cvs')
        obj.required_skills = serializer.validated_data.get('required_skills')
        obj.required_work_experience = serializer.validated_data.get('required_work_experience')
        obj.required_soft_skills = serializer.validated_data.get('required_soft_skills')
        obj.required_languages = serializer.validated_data.get('required_languages')
        obj.expire_time = serializer.validated_data.get('expire_time')
        obj.status = serializer.validated_data.get('status')
        obj.save()

        response_data = JobSerializer(obj).data
        return Response(response_data, status.HTTP_200_OK)
    else:
        response_data = {
            'message': 'validation error',
            'data': serializer.errors
        }
        return Response(response_data, status.HTTP_422_UNPROCESSABLE_ENTITY)
    

# 5
# delete job
#
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['company'])
def job_delete(request, id):
    Job.objects.get(id = id).delete()
    response_data = {
        "message": "Job Deleted Successfully"
    }
    return Response(response_data, status.HTTP_200_OK)



# 6
# show employee profile
#
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['company'])
def show_profile(request, id):
    data = EmployeeProfile.objects.get(employee_id = id)
    serializer = EmployeeProfileSerializer(data)
    
    return Response(serializer.data, status.HTTP_200_OK)