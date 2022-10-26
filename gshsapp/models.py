from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Gubun(models.Model):
    GUBUN = (
        ('Buyproduct', '구매Table'),
        ('Replacement', '교체Table'),        
    )
    tablename = models.CharField(max_length=20, default='', choices=GUBUN)
    gubun = models.CharField(max_length=50)

    def __str__(self):
        return self.gubun

class Buyproduct(models.Model):
    buydate = models.DateField(default=timezone.now)
    gubun = models.ForeignKey(Gubun, on_delete=models.CASCADE, related_name='buyproduct')
    company = models.CharField(max_length=20)
    model = models.CharField(max_length=30)    
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'[{self.gubun.gubun}] {self.model}'

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
    LGUBUN = (
        ('부서','부서'),
        ('강의실','강의실'),
        ('실험실','실험실'),
        ('협의회실','협의회실'),
        ('강당','강당'),
        ('기타','기타'),
    )
    building = models.CharField(max_length=50)
    hosil = models.CharField(max_length=20) 
    locationgubun = models.CharField(max_length=20, default='기타', choices=LGUBUN)   
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'[{self.building}] {self.hosil}'

class Gigiinfo(models.Model):
    COLOR_SELECT = (
        ('None',None),
        ('블랙','블랙'),
        ('컬러','컬러'),
    )
    buyproduct = models.ForeignKey(Buyproduct, on_delete=models.CASCADE, related_name='gigiinfo')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='gigiinfo')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigiinfo', null=True, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=10, choices=COLOR_SELECT, default=None, blank=True)
    jaego = models.BooleanField(default=False)
    notuse = models.BooleanField(default=False)
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.location} / {self.buyproduct} / {self.user}'

class Repair(models.Model):
    date = models.DateField(default=timezone.now)
    gigiinfo = models.ForeignKey(Gigiinfo, on_delete=models.CASCADE, related_name='repair')
    problem = models.CharField(max_length=50)
    result = models.CharField(max_length=50)
    cost = models.PositiveIntegerField(default=0)
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.gigiinfo)

class Replacement(models.Model):
    date = models.DateField(default=timezone.now)
    gigiinfo = models.ForeignKey(Gigiinfo, on_delete=models.CASCADE, related_name='replacement')
    gubun = models.ForeignKey(Gubun, on_delete=models.CASCADE, related_name='replacement')
    count = models.PositiveSmallIntegerField(default=1)
    cost = models.PositiveIntegerField(default=0)
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.gigiinfo)

# def get_image_filename(instance, filename):
#     id = instance.repair.id
#     return "images/%Y/%m/%d/%s" % (id)  

class Repair_Photo(models.Model):
    repair = models.ForeignKey(Repair, default=None, on_delete=models.CASCADE, related_name="repair_photo")
    image = models.ImageField(upload_to="images/%Y/%m/%d/")

    def __str__(self):
        return str(self.repair)


class Change_Photo(models.Model):
    replacement = models.ForeignKey(Replacement, default=None, on_delete=models.CASCADE, related_name="change_photo")
    image = models.ImageField(upload_to="images/%Y/%m/%d/")

    def __str__(self):
        return str(self.replacement)


class Memo(models.Model):
    pass

class Freeboard(models.Model):
    pass