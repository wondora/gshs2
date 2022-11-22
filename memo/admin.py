from django.contrib import admin
from .models import Memo

class MemoAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Memo, MemoAdmin)
