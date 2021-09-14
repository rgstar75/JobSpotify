from django.db import models
# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
#from django.db.models.deletion import CASCADE

class Job(models.Model):
    recruiter=models.ForeignKey(User,related_name='jobs',on_delete=models.CASCADE)
    job_title=models.CharField(max_length=200)
    company_name=models.CharField(max_length=200)
    job_description=models.CharField(max_length=500)
    skills=models.CharField(max_length=500)
    job_type=models.CharField(max_length=200)
    end_date=models.DateField(default=timezone.now)
    posted_on=models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.job_title
    
class Applicants(models.Model):
    job = models.ForeignKey(
        Job, related_name='applicants', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='applied', on_delete=models.CASCADE)
    
        
    def __int__(self):
        return self.applicant


class SelectedApplicants(models.Model):
    job = models.ForeignKey(
        Job, related_name='select_job', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='select_applicant', on_delete=models.CASCADE)

    def __int__(self):
        return self.applicant
