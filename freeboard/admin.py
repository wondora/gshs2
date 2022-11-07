from django.contrib import admin
from .models import Freeboard

class FreeboardAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'writer', 
        'hits',
        'registered_date',
        )
    search_fields = ('title', 'content', 'writer__username',)

admin.site.register(Freeboard, FreeboardAdmin)