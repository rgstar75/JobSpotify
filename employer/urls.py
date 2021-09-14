from django import views
from django.contrib import admin
from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
  
    path('',views.HomeView,name='home1'),
   path('postjob',views.postjob,name='postjob'),
   path('jobdetail/<int:id>',views.details_of_job,name='jobdetail_recruiter'), 
    path('applicants/<int:id>',views.applicant,name='applicants'),
     path('selected/<int:id>',views.selected,name='selected'),
   path('select/<int:job_id>/<int:applicant_id>',views.slelectapplicant,name='select'),
      path('remove/<int:job_id>/<int:applicant_id>',views.removeapplicant,name='remove'),
      path('editjob/<int:id>',views.edit_job,name='editjob'),
      path('applicantdetails/<int:applicant_id>',views.applicantprofile,name='applicantprofile')


   
    

    
]