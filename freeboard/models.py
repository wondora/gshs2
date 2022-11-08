import os
from django.conf import settings
from django.db import models
from uuid import uuid4
from datetime import datetime

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file', ymd_path, uuid_name])


class Freeboard(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    title = models.CharField(max_length=128, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    registered_date = models.DateField(auto_now_add=True, verbose_name='등록시간')
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'freeboard'
