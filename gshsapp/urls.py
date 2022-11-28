from django.urls import path
from . import views

app_name = 'gshsapp'

urlpatterns = [
    path('<str:gigigubun>/', views.InfogigiList, name='gigi_gubun'),
    path('create/<int:pk>/', views.InfogigiCV.as_view(), name='gigi_create'),
    path('delete/<int:pk>/', views.InfogigiDel, name='gigi_delete'),
    path('update/<int:pk>/', views.InfogigiUV.as_view(), name='gigi_update'),
    path('change/<int:pk>/', views.InfogigiChange, name='gigi_change'),
    path('suri/<int:pk>/', views.InfogigiSuri, name='gigi_suri'),  
    # path('search/<str:gigigubun>/', views.InfogigiSearch, name='gigi_search'),  
    path('buseo/<str:buseogubun>/', views.InfogigiBuseo, name='gigi_buseo'), 
    # path('buseo/change/photo/', views.ChangePhotoAjax, name='changephoto_up'), 
    path('buseo/update/<int:pk>/', views.InfogigiBuseoUpdate, name='gigi_buseo_update'), 
    path('buseo/cr/update/<int:pk>/', views.buseoCRUpdate, name='buseo_CR_update'), 
    path('buseo/cr/delete/<int:pk>/', views.buseoCRUdelete, name='buseo_CR_delete'), 
    path('excel/<str:gubun>/', views.excelExport, name='excelExport'), 
]
