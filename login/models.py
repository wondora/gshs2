from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=50, null=True)