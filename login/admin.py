from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from .models import User

class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('username', 'name', 'subject')

admin.site.register(User, UserAdmin)

