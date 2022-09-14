from django.contrib import admin
from django.urls import path
import gshsapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', gshsapp.views.home, name='home'),
]