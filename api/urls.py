# from xml.etree.ElementInclude import include
from django.urls import include
from django.urls import path
from api.views.AuthView import *
from api.views.CompanyView import *
from api.views.EmployeeView import * 
app_name = 'api'


# extra_patterns = [
#     path('test', test, name='test')
# ]

urlpatterns = [
    # Authintication Urls
    path('registration/employee/', EmployeeRegistrationView.as_view(), name='register-employee'),
    path('registration/company/', CompanyRegistrationView.as_view(), name='register-company'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Employee Urls
    path('employee/', include([
        path('profile/', retrive_profile),
        path('profile/<id>', update_profile),
        path('jobs/', jobs_all),
        path('jobs/<id>', job_details),
        path('jobs/apply/', apply_job),
        path('jobs/cansel-apply/<id>', cansel_apply),
    ])),
    
    # Company Urls
    path('company/', include([
        path('jobs/', job_list),
        path('jobs/<id>', job_details),
        path('jobs/create/', job_create),
        path('jobs/update/<id>', job_update),
        path('jobs/delete/<id>', job_delete),
        path('employee/show-profile/<id>', show_profile),
    ]))
]

