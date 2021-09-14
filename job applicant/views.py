from django.db import models
from django.db.models import query
from django.http.response import HttpResponseRedirect
from django.shortcuts import  render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import  redirect
from .models import *
from recruiter.models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
import json
from .forms import ProfileForm
from django.http import JsonResponse,HttpResponse
User=get_user_model()

def HomeView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    jobs=Job.objects.all()
    paginator=Paginator(jobs,5)
    page_number  = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context={
        'page_obj':page_obj,
        'jobs':jobs
    }
    return render(request,'applicant/home.html',context)

def applied_jobs(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=request.user
    status=[]
  
    jobs=AppliedJobs.objects.filter(user=user)
    for job in jobs:
        if Applicants.objects.filter(job=job.job).filter(applicant=user).exists():
            status.append('pending')
        elif SelectedApplicants.objects.filter(job=job.job).filter(applicant=user).exists():
            status.append('selected')
        else:
            status.append('rejected')
            
    zipd=zip(jobs,status)

    print(status)
    return render(request,'applicant/applied.html',{'zipd':zipd})

def details_of_job(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    job=Job.objects.get(pk=id)
    applied=False
    if AppliedJobs.objects.filter(user=request.user).filter(job=job).exists():
        applied=True
    
    context={
        'job':job,
        'applied':applied
    }   
    return render(request,'applicant/jobdetail.html',context)


def apply(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    user=request.user
    job=Job.objects.get(pk=id)
    applied=True
    apply=Applicants(job=job,applicant=user)
    add_to_applied=AppliedJobs(user=user,job=job)
    apply.save()
    add_to_applied.save()
    
    return render(request,'applicant/jobdetail.html',{'job':job,'applied':applied})

def search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':

        search_str=json.loads(request.body).get('searchText')
        job=Job.objects.filter(
            job_type__icontains=search_str) | Job.objects.filter(
            company_name__icontains=search_str)
        data=job.values()
        return JsonResponse(list(data),safe=False)
    
def logout(request):
    return redirect('/')

def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile=ApplicantProfile.objects.filter(user=request.user).first()
    context={
        'user':request.user,
        'profile':profile
    }
    return render(request,'applicant/profile.html',context)

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=request.user
    profile=ApplicantProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            data=form.save(commit=False)
            data.user=user
            data.save()
            return redirect('profile')
    else:
        form=ProfileForm(instance=profile)
    return render(request,'applicant/editprofile.html',{'form':form})
    
    
    
    
    

    
    



    
    


