from django import forms
from django.forms import fields
from .models import ApplicantProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model=ApplicantProfile
        fields=['name','email','gender','birth_date','resume']