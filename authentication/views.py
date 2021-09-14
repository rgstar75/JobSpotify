from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from validate_email import validate_email
from django.contrib import auth
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
from django.core.mail import EmailMessage
import json
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse
class EmailThread(threading.Thread):
    def __init__(self, email ):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently=False)

class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'},status = 400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error': 'email already exists'},status = 400)
        return JsonResponse({'email_valid': True})        

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'},status = 400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'username already exists'},status = 400)
        return JsonResponse({'username_valid': True})

class applicant_register(View):
    def get(self, request):
        return render(request, 'authentication/applicant_register.html')
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password']
        context = {
            'fieldValues': request.POST
        }
        if password!=password2:
            messages.error(request, 'password does not match')
            return render(request, 'authentication/applicant_register.html', context)
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request, 'password too short')
                    return render(request, 'authentication/applicant_register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                usertype=Applicant.objects.create(user=user)
                usertype.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                EmailThread(email).start()
                messages.success(request, 'Hi there, please go through verification mail to activate your account')
                return render(request, 'authentication/login.html')
            messages.error(request, 'email already exists')
        messages.error(request,'user already exists')
        return redirect('login')

class recruiter_register(View):
    def get(self, request):
        return render(request, 'authentication/recruiter_register.html')
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password']
        context = {
            'fieldValues': request.POST
        }
        if password!=password2:
            messages.error(request, 'password does not match')
            return render(request, 'authentication/recruiter_register.html', context)
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request, 'password too short')
                    return render(request, 'authentication/recruiter_register.html', context)
                user = User.objects.create_user(username=username, email=email)
                usertype=Recruiter.objects.create(user=user)
                usertype.save()
                user.set_password(password)
                user.is_active =False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link
                print(activate_url)
                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                EmailThread(email).start()
                messages.success(request, 'Hi there, please go through verification mail to activate your account')
                return render(request, 'authentication/login.html')
            messages.error(request, 'email already exists')
        messages.error(request,'user already exists')
        return render( request, 'authentication/recruiter_register.html')
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                messages.info(request,'User already activated')
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')
   
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user and Applicant.objects.filter(user=user).exists():
                auth.login(request, user)
                messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                return redirect('home')
            
            elif user and Recruiter.objects.filter(user=user).exists():
                auth.login(request,user)
                messages.success(request,'welcome,'+user.username+'you are now logged in')
                return redirect('home1')
            else:
                messages.error(request,'please register')
            
            messages.error(
            request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
        request, 'Please fill all fields')
        return render(request, 'authentication/login.html')
class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')
    def post(self,request):
        email = request.POST['email']
        context = {
        'values': request.POST
        }
        if not validate_email(email):
            messages.error(request,'Please provide a valid email')
            return render(request,'authentication/reset-password.html',context)
        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
        if user:
            email_contents = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password', kwargs={
                           'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Password reset Instructions'

            reset_url = 'http://'+current_site.domain+link
            email = EmailMessage(
                email_subject,
                'Hi there, Please click on the link below to reset your password \n'+reset_url,
                'noreply@semycolon.com',
                [email],
            )
            EmailThread(email).start()
        messages.success(request, "Check your email")

        return render(request,'authentication/reset-password.html')

class CompletePasswordReset(View):
    def get(self,request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None or not token_generator.check_token(user, token):
            messages.add_message(
                request, messages.WARNING, 'Link is no longer valid,please request a new one')
            return render(request, 'authentication/reset-password.html', status=401)
        return render(request, 'authentication/set-new-password.html', context={'uidb64': uidb64, 'token': token})
    def post(self, request, uidb64, token):
        context = {'uidb64': uidb64, 'token': token}
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if len(password) < 6:
                messages.add_message(
                    request, messages.ERROR, 'Password should be at least 6 characters long')
                return render(request, 'authentication/set-new-password.html', context, status=400)
            if password != password2:
                messages.add_message(
                    request, messages.ERROR, 'Passwords must match')
                return render(request, 'authentication/set-new-password.html', context, status=400)
            user.set_password(password)
            user.save()
            messages.add_message(
                request, messages.INFO, 'Password changed successfully,login with your new password')
            return redirect('login')
        except DjangoUnicodeDecodeError:
            messages.add_message(
                request, messages.ERROR, 'Something went wrong,you could not update your password')
            return render(request, 'authentication/set-new-password.html', context, status=401)

def logout(request):
    auth.logout(request)
    return redirect('/')   

