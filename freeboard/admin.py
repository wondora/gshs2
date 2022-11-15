from django.contrib import admin
from .models import Freeboard, Comment

class FreeboardAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'writer', 
        'hits',
        'registered_date',
        )
    search_fields = ('title', 'content', 'writer__username',)

admin.site.register(Freeboard, FreeboardAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post', 
        'content',
        'writer',
        'created',
        'deleted',
    )
    search_fields = ('post__title', 'content', 'writer__user_id',)

admin.site.register(Comment, CommentAdmin)