from django.urls import path
from . import views

app_name = 'gshsapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('gigi/<str:gigigubun>/', views.InfogigiLV.as_view(), name='gigi_gubun'),
    path('gigi/update/<int:pk>/', views.InfogigiUV.as_view(), name='gigi_update'),
    path('gigi/change/<int:pk>/', views.InfogigiChange, name='gigi_change'),
    path('gigi/suri/<int:pk>/', views.InfogigiSuri, name='gigi_suri'),  
]
