from django import forms
from django.forms import fields
from .models import Job

class JobDetails(forms.ModelForm):
    class Meta:
        model=Job
        fields=['job_title','company_name','job_description','skills','job_type','end_date','posted_on']