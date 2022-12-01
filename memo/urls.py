from django.urls import path
from . import views

app_name = 'memo'

urlpatterns = [
    path('list/', views.memo, name='memo'),
    path('write/', views.create_memo, name='create_memo'),
    path('delete/<int:pk>', views.delete_memo, name='delete_memo'),
]