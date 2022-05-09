from os import stat
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.decorators import required_roles
from api.models import *
from api.serializers.CompanySerializer import *
from ..serializers.EmployeeSerializer import *
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

##### Profile Functions
#####################################################################################

# 1
# get profile of current user
#
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['employee'])
def retrive_profile(request):
    try:
        query = EmployeeProfile.objects.get(employee = request.user.employee)
    except EmployeeProfile.DoesNotExist:
        query = EmployeeProfile.objects.create(employee = request.user.employee)

    serializer = EmployeeProfileSerializer(query)
    return Response(serializer.data)


# 2
# update profile of current user
#
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['employee'])
def update_profile(request, id):
    serializer = EmployeeProfileSerializer(data = request.data)
    if (serializer.is_valid()):
        obj = EmployeeProfile.objects.get(id = id)
        obj.image = serializer.validated_data.get('image')
        obj.phone = serializer.validated_data.get('phone')
        obj.address = serializer.validated_data.get('address')
        obj.birthdate = serializer.validated_data.get('birthdate')
        obj.skills = serializer.validated_data.get('skills')
        obj.previous_works = serializer.validated_data.get('previous_works')
        obj.languages = serializer.validated_data.get('languages')
        obj.softskills = serializer.validated_data.get('softskills')
        obj.cv = serializer.validated_data.get('cv')
        obj.save()
 
        response_data = EmployeeProfileSerializer(obj).data
        return Response(response_data, status.HTTP_200_OK)

    else:
        response_data = {
            'message': 'validation error',
            'data': serializer.errors
        }
        return Response(response_data, status.HTTP_422_UNPROCESSABLE_ENTITY)
    


##### Jobs Functions
#####################################################################################

# 3
# get all jobs
#
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['employee'])
def jobs_all(request):
    data = Job.objects.all()
    serializer = JobSerializer(data, many= True)
    return Response(serializer.data, status.HTTP_200_OK)

# 4
# apply for job
#
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['employee'])
def apply_job(request):
    data = JobApplicant.objects.create(
        job = Job.objects.get(id = request.data['job_id']),
        employee = Employee.objects.get(id = request.data['employee_id']), 
        email = Employee.objects.get(id = request.data['employee_id']).employee.email
    )
    respons_data = JobApplicantSerializer(data).data
    return Response(respons_data, status.HTTP_200_OK)


# 5
# cansel apply 
#
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['employee'])
def cansel_apply(request, id):
    employee_id = request.user.employee.id
    JobApplicant.objects.get(employee_id = employee_id, job_id = id).delete()

    response_data = {
        'message': 'apply job canseled'
    }
    return Response(response_data, status.HTTP_200_OK)

