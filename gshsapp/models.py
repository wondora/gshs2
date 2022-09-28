from django.db import models
from django.contrib.auth.models import AbstractUser


class Buyproduct(models.Model):
    buydate = models.DateField
    bcategory = models.CharField(max_length=20)
    company = models.CharField(max_length=20)
    model = models.CharField(max_length=30)    
    bigo = models.CharField(max_length=60, Null=True)

class User(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50, null=True)

class Location(models.Model):
    building = models.CharField(max_length=50)
    hosil = models.CharField(max_length=20)
    lcategory = models.CharField(max_length=20)
    bigo = models.CharField(max_length=60, Null=True)

class Gigiinfo(models.Model):
    buyproduct = models.ForeignKey(Buyproduct)
    location = models.ForeignKey(Location)
    user = models.ForeignKey(User)
    ip = models.CharField(20)
    color = models.BooleanField(default=False)
    jaego = models.BooleanField(default=False)
    notuse = models.BooleanField(default=False)
    bigo = models.CharField(max_length=60, Null=True)

class Repair(models.Model):
    date = models.DateField(auto_now_add=True)
    gigiinfo = models.ForeignKey(Gigiinfo)
    problem = models.CharField(max_length=50)
    result = models.CharField(max_length=50)
    cost = models.PositiveIntegerField
    image = models.ImageField
    bigo = models.CharField(max_length=60, Null=True)

class Bupum(models.Model):
    bupum = models.CharField(max_length=20)

class Replacement(models.Model):
    date = models.DateField(auto_now_add=True)
    gigiinfo = models.ForeignKey(Gigiinfo)
    bupum = models.ForeignKey(Bupum)
    count = models.PositiveSmallIntegerField
    cost = models.PositiveIntegerField
    bigo = models.CharField(max_length=60, Null=True)

class Memo(models.Model):
    pass

class Freeboard(models.Model):
    pass