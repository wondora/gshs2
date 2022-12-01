from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from .models import *

class Repair_PhotoInline(admin.TabularInline):
    model = Repair_Photo

class RepairAdmin(admin.ModelAdmin):
    inlines = [Repair_PhotoInline, ]
    list_display = ['id', 'date', 'gigiinfo', 'problem', 'result', 'cost', 'bigo']

admin.site.register(Repair, RepairAdmin)

class Change_PhotoInline(admin.TabularInline):
    model = Change_Photo

class ReplacementAdmin(admin.ModelAdmin):
    inlines = [Change_PhotoInline, ]
    list_display = ['id', 'date', 'gigiinfo', 'gubun', 'count', 'cost', 'bigo']

admin.site.register(Replacement, ReplacementAdmin)


class BuyproductAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'company', 'model', 'bigo']

admin.site.register(Buyproduct, BuyproductAdmin)


class LocationAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'building', 'hosil', 'locationgubun', 'bigo']
admin.site.register(Location, LocationAdmin)


class GigiinfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'date','buyproduct', 'location', 'user', 'ip', 'color', 'jaego', 'notuse', 'bigo']
admin.site.register(Gigiinfo, GigiinfoAdmin)


class GubunAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'tablename', 'gubun']
admin.site.register(Gubun, GubunAdmin)

# class RepairAdmin(admin.ModelAdmin):
#     list_display = ['id', 'date', 'gigiinfo', 'problem', 'result', 'cost', 'bigo']

# class ReplacementAdmin(admin.ModelAdmin):
#     list_display = ['id', 'date', 'gigiinfo', 'gubun', 'count', 'cost', 'bigo']


class Change_PhototAdmin(admin.ModelAdmin):
    list_display = ['id', 'replacement', 'image']
admin.site.register(Change_Photo, Change_PhototAdmin)

class Repair_PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'repair', 'image']
admin.site.register(Repair_Photo, Repair_PhotoAdmin)
