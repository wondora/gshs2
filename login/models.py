from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = None
    last_name = None
    password = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, unique=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)  
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user"