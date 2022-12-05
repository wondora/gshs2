from django.urls import path
from . import views

app_name = 'gshsapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('gigi/<str:gigigubun>/', views.InfogigiList, name='gigi_gubun'),
    path('gigi/create/<str:gigigubun>/', views.InfogigiCV.as_view(), name='gigi_create'),
    path('gigi/delete/<int:pk>/', views.InfogigiDel, name='gigi_delete'),
    path('gigi/update/<int:pk>/', views.InfogigiUV.as_view(), name='gigi_update'),
    path('gigi/change/<int:pk>/', views.InfogigiChange, name='gigi_change'),
    path('gigi/suri/<int:pk>/', views.InfogigiSuri, name='gigi_suri'),  
    path('gigi/buseo/<str:buseogubun>/', views.InfogigiBuseo, name='gigi_buseo'), 
    path('gigi/buseo/update/<int:pk>/', views.InfogigiBuseoUpdate, name='gigi_buseo_update'), 
    path('gigi/buseo/cr/update/<int:pk>/', views.buseoCRUpdate, name='buseo_CR_update'), 
    path('gigi/buseo/cr/delete/<int:pk>/', views.buseoCRUdelete, name='buseo_CR_delete'), 
    path('gigi/excel/<str:gubun>/', views.excelExport, name='excelExport'), 
]
