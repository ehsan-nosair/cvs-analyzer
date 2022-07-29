from api.decorators import required_roles
from .AuthView import *
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_auth.registration.views import RegisterView
from api.models import User

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from api.serializers import (
    EmployeeCustomRegistrationSerializer, CompanyCustomRegistrationSerializer
    )


##comment for testing

# Employee Register
######################################################################################
class EmployeeRegistrationView(RegisterView):
    serializer_class = EmployeeCustomRegistrationSerializer



# Company Register
######################################################################################
class CompanyRegistrationView(RegisterView):
    serializer_class = CompanyCustomRegistrationSerializer



# Login Employee & Company
######################################################################################
# @csrf_exempt
@api_view(['POST'])
def login_user(request):
        data = {}
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            Account = User.objects.get(email=str(email))
        except BaseException as e:
            responseData = {"message": "User matching query does not exist"}
            return Response(responseData, status.HTTP_400_BAD_REQUEST)


        token = Token.objects.get_or_create(user=Account)[0].key


        if not check_password(password, Account.password):
            responseData = {"message": "Incorrect Login credentials"}
            return Response(responseData, status.HTTP_400_BAD_REQUEST)

        if Account:
            if Account.is_active:
                login(request, Account)
                data["message"] = "user logged in"
                data["id"] = Account.id
                data["email_address"] = Account.email
                if Account.is_employee:
                    data["role"] = "employee"
                elif Account.is_company:
                    data["role"] = "company"    

                responseData = {"data": data, "token": token}
                return Response(responseData, status.HTTP_200_OK)

            else:
                responseData = {"message": "Account not active"}
                return Response(responseData, status.HTTP_400_BAD_REQUEST)

        else:
            responseData = {"message": "Account doesnt exist"}
            
            return Response(responseData, status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@required_roles(['employee', 'company'])
def logout_user(request):
    request.user.auth_token.delete()
    response_data = {
        "message": "logout success"
    }
    return Response(response_data, status.HTTP_200_OK)