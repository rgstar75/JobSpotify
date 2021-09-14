from django.contrib import admin
from django.urls import path,include
from .views import *
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
      path('applicant', applicant_register.as_view(), name = 'applicant'),
      path('recruiter', recruiter_register.as_view(), name = 'recruiter'),
      path('login', LoginView.as_view(), name = 'login'),
      path('logout',views.logout,name='logout'),
      path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
         name="validate-username"),
      path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate_email'),
      path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
      path('set-new-password/<uidb64>/<token>',
             CompletePasswordReset.as_view(), name='reset-user-password'),
      path('request-reset-link',RequestPasswordResetEmail.as_view(),name="request-password")

]