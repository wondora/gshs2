from django.urls import path
from . import views

app_name = 'gshsapp'

urlpatterns = [
    path('', views.home, name='home'),
]
