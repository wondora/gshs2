from django.db import models
from django.contrib.auth.models import AbstractUser

class Gubun(models.Model):
    tablename = models.CharField(max_length=20, default='')
    gubun = models.CharField(max_length=50)

    def __str__(self):
        return self.gubun

class Buyproduct(models.Model):
    buydate = models.DateField
    gubun = models.ForeignKey(Gubun, on_delete=models.CASCADE, related_name='buyproduct')
    company = models.CharField(max_length=20)
    model = models.CharField(max_length=30)    
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.model

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

class Location(models.Model):
    building = models.CharField(max_length=50)
    hosil = models.CharField(max_length=20)    
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.hosil

class Gigiinfo(models.Model):
    buyproduct = models.ForeignKey(Buyproduct, on_delete=models.CASCADE, related_name='gigiinfo')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='gigiinfo')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigiinfo', null=True, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    color = models.BooleanField(default=False)
    jaego = models.BooleanField(default=False)
    notuse = models.BooleanField(default=False)
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.location.hosil

class Repair(models.Model):
    date = models.DateField(auto_now_add=True)
    gigiinfo = models.ForeignKey(Gigiinfo, on_delete=models.CASCADE, related_name='repair')
    problem = models.CharField(max_length=50)
    result = models.CharField(max_length=50)
    cost = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='repair/', null=True, blank=True)
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.gigiinfo

class Replacement(models.Model):
    date = models.DateField(auto_now_add=True)
    gigiinfo = models.ForeignKey(Gigiinfo, on_delete=models.CASCADE, related_name='replacement')
    gubun = models.ForeignKey(Gubun, on_delete=models.CASCADE, related_name='replacement')
    count = models.PositiveSmallIntegerField(default=1)
    cost = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='replacement/', null=True, blank=True)
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.gigiinfo

class Memo(models.Model):
    pass

class Freeboard(models.Model):
    pass