from django.urls import path
from . import views

app_name = 'freeboard'

urlpatterns = [
    path('', views.FreeboardListView.as_view(), name='freeboard_list'),
    path('<int:pk>/', views.freeboard_detail_view, name='freeboard_detail'),
    path('write/', views.freeboard_write_view, name='freeboard_write'),
    path('<int:pk>/edit/', views.freeboard_edit_view, name='freeboard_edit'),
    path('<int:pk>/delete/', views.freeboard_delete_view, name='freeboard_delete'),
    path('download/<int:pk>', views.freeboard_download_view, name="freeboard_download"),
]