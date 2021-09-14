from django import views
from django.contrib import admin
from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
  
    path('',views.HomeView,name='home'),
    path('applied',views.applied_jobs,name='applied'),
    path('jobdetail/<int:id>',views.details_of_job,name='jobdetail'),
    path('apply/<int:id>',views.apply,name='apply'),
    path('search', csrf_exempt(views.search), name = "search"),
    path('profile',views.my_profile,name='profile'),
    path('edit_profile',views.edit_profile,name='editprofile')
    

    
]