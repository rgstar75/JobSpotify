from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.
import datetime
from recruiter.models import Job

class ApplicantProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='ApllicantProfile',primary_key=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    gender=models.CharField(max_length=10,null=True)
    birth_date=models.DateField()
    resume=models.FileField(upload_to='resume')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.user.username
    
    
class AppliedJobs(models.Model):
    user=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    job=models.ForeignKey(Job,related_name='job',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.job.job_title
    
    
    