from django.db import models
from django.utils import timezone
import os
from django.conf import settings
from login.models import User


class Gubun(models.Model):
    GUBUN = (
        ('Buyproduct', '구매Table'),
        ('Replacement', '교체Table'),        
        ('Repair', '수리Table'),        
    )
    tablename = models.CharField(max_length=20, default='', choices=GUBUN)
    gubun = models.CharField(max_length=50)

    def __str__(self):
        return self.gubun

    class Meta:
        db_table = "gubun"

class Buyproduct(models.Model):  
    gubun = models.ForeignKey(Gubun, on_delete=models.CASCADE, related_name='buyproduct')
    company = models.CharField(max_length=20)
    model = models.CharField(max_length=30)    
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'[{self.gubun}] {self.model}'

    class Meta:
        db_table = "buyproduct"

class Location(models.Model):
    LGUBUN = (
        ('부서','부서'),
        ('강의실','강의실'),
        ('실험실','실험실'),
        ('협의회실','협의회실'),
        ('강당','강당'),
        ('서버실','서버실'),
        ('Wee클래스','Wee클래스'),
        ('동아리실','동아리실'),
        ('기타','기타'),
    )
    BGUBUN = (
        ('본관','본관'),
        ('SRC','SRC'),
        ('학술정보관','학술정보관'),
        ('학습관','학습관'),
        ('자치관','자치관'),
        ('창조관','창조관'),
        ('급식소','급식소'),
        ('우정1관','우정1관'),
        ('우정2관','우정2관'),
        ('아름관','아름관'),
    )
    building = models.CharField(max_length=50, choices=BGUBUN)
    hosil = models.CharField(max_length=20) 
    locationgubun = models.CharField(max_length=20, default='기타', choices=LGUBUN)   
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'[{self.building}] {self.hosil}'

    class Meta:
        db_table = "location"


class Gigiinfo(models.Model):
    COLOR_SELECT = (
        ('None',None),
        ('블랙','블랙'),
        ('컬러','컬러'),
    )
    date = models.DateField(default=timezone.now)
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

    class Meta:
        db_table = "gigiinfo"


class Repair(models.Model):
    date = models.DateField(default=timezone.now)
    gigiinfo = models.ForeignKey(Gigiinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='repair')
    problem = models.CharField(max_length=50)
    result = models.CharField(max_length=50)
    cost = models.PositiveIntegerField(default=0)
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.gigiinfo)

    def delete(self, *args, **kargs):
        rep = Repair.objects.get(id=self.id)
        this = rep.repair_photo.all()
        for i in this:
            i.delete()
        return super().delete(*args, **kargs)

    class Meta:
        db_table = "repair"


class Replacement(models.Model):
    date = models.DateField(default=timezone.now)
    gigiinfo = models.ForeignKey(Gigiinfo, null=True, blank=True, on_delete=models.CASCADE, related_name='replacement')
    gubun = models.ForeignKey(Gubun, on_delete=models.CASCADE, related_name='replacement')
    count = models.PositiveSmallIntegerField(default=1)
    cost = models.PositiveIntegerField(default=0)
    bigo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.gigiinfo)

    def delete(self, *args, **kargs):
        rep = Replacement.objects.get(id=self.id)
        this = rep.change_photo.all()
        for i in this:
            i.delete()
        return super().delete(*args, **kargs)

    class Meta:
        db_table = "replacement"

# def get_image_filename(instance, filename):
#     id = instance.repair.id
#     return "images/%Y/%m/%d/%s" % (id)  

class Repair_Photo(models.Model):
    repair = models.ForeignKey(Repair, default=None, on_delete=models.CASCADE, related_name="repair_photo")
    image = models.ImageField(upload_to="images/%Y/%m/%d/")

    def __str__(self):
        return str(self.repair)

    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
            super().delete(*args, **kargs)

    class Meta:
        db_table = "repair_Photo"


class Change_Photo(models.Model):
    replacement = models.ForeignKey(Replacement, default=None, on_delete=models.CASCADE, related_name="change_photo")
    image = models.ImageField(upload_to="images/%Y/%m/%d/")

    def __str__(self):
        return str(self.replacement)

    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
            super().delete(*args, **kargs)

    class Meta:
        db_table = "change_Photo"
