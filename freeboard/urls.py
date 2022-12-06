from django.urls import path
from . import views

app_name = 'freeboard'

urlpatterns = [
    path('list/', views.AllListView.as_view(), name='all_list'),
    path('free/', views.FreeListView.as_view(), name='freeboard_list'),
    path('gshs/', views.GshsListView.as_view(), name='gshs_list'),
    path('linux/', views.LinuxListView.as_view(), name='linux_list'),
    path('window/', views.WindowListView.as_view(), name='window_list'),
    path('window/', views.CodeListView.as_view(), name='code_list'),

    path('<int:pk>/', views.freeboard_detail_view, name='freeboard_detail'),
    path('write/', views.freeboard_write_view, name='freeboard_write'),
    path('<int:pk>/edit/', views.freeboard_edit_view, name='freeboard_edit'),
    path('<int:pk>/delete/', views.freeboard_delete_view, name='freeboard_delete'),
    path('download/<int:pk>', views.freeboard_download_view, name="freeboard_download"),
    path('<int:pk>/comment/write/', views.comment_write_view, name='comment_write'),
    path('<int:pk>/comment/delete/', views.comment_delete_view, name='comment_delete'),
]