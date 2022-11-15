import os
from django.conf import settings
from django.db import models
from uuid import uuid4
import pytz 
from datetime import datetime, timedelta
from django.utils import timezone

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file', ymd_path, uuid_name])

CATEGORY_CHOICES = (
    ("자유", "자유"),
    ("GSHS", "학교"),
    ("LINUX", "리눅스"),
    ("WINDOW", "윈도우"),
)

class Freeboard(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    title = models.CharField(max_length=128, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=18, verbose_name='분류', default='자유')
    upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    comments = models.PositiveIntegerField(verbose_name='댓글수', null=True)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'freeboard'

    def delete(self, *args, **kargs):
        if self.upload_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
        super().delete(*args, **kargs)

    @property
    def created_string(self):

        time = datetime.now() - self.registered_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now().date() - self.registered_date.date()
            return str(time.days) + '일 전'
        else:
            return False


class Comment(models.Model):
    post = models.ForeignKey(Freeboard, on_delete=models.CASCADE, verbose_name='게시글')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='댓글작성자')
    content = models.TextField(verbose_name='댓글내용')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    deleted = models.BooleanField(default=False, verbose_name='삭제여부')
    reply = models.IntegerField(verbose_name='답글위치', default=0)
    
    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comment'
        verbose_name = '자유게시판 댓글'
        verbose_name_plural = 'comments'

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.kst) - self.created

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.kst).date() - self.created.date()
            return str(time.days) + '일 전'
        else:
            return False
