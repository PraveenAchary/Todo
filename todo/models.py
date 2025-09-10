from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tasks(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    taskname = models.CharField(max_length=50,default="You are Free Today!")
    deadline = models.DateField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)