from django.contrib import admin
from .models import *

class Repair_PhotoInline(admin.TabularInline):
    model = Repair_Photo

class RepairAdmin(admin.ModelAdmin):
    inlines = [Repair_PhotoInline, ]


class Change_PhotoInline(admin.TabularInline):
    model = Change_Photo

class ReplacementAdmin(admin.ModelAdmin):
    inlines = [Change_PhotoInline, ]

admin.site.register(User)
admin.site.register(Buyproduct)
admin.site.register(Location)
admin.site.register(Gigiinfo)
admin.site.register(Gubun)
admin.site.register(Repair, RepairAdmin)
admin.site.register(Replacement, ReplacementAdmin)
admin.site.register(Change_Photo)
admin.site.register(Repair_Photo)
