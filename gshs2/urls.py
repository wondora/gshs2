from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#URL로 MEDIA_ROOT에 접근하여 강제적으로 파일을 다운, 이미지파일 등에 접근하는 것을 방지
# def protected_file(request, path, document_root=None):
#     messages.error(request, "접근 불가")
#     return redirect('/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gshsapp.urls')),
    # path('gigi/', include('gshsapp.urls')),
    path('auth/', include('login.urls')),
    path('freeboard/', include('freeboard.urls')),
    path('memo/', include('memo.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)