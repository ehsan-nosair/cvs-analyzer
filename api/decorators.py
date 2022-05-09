
from rest_framework.response import Response
from rest_framework import status


def required_roles(rols = []):
    def wrapper(view_func):
        def wrapped(request, *args, **kwargs):
            if request.user.is_admin and 'admin' in rols:
                return view_func(request, *args, **kwargs)
            if request.user.is_employee and 'employee' in rols:
                return view_func(request, *args, **kwargs)
            if request.user.is_company and 'company' in rols:
                return view_func(request, *args, **kwargs)
            else:
                return Response(
                    {'message' : 'Un Authorized User'},
                    status.HTTP_401_UNAUTHORIZED
                )
        return wrapped
    return wrapper