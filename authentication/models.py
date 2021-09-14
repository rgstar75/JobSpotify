from django.db import models

from django.contrib.auth.models import User
from django.db.models.enums import Choices


class Recruiter(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class Applicant(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
