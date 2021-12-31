from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('counteye.urls', namespace='counteye')),
    path('api/', include('counteyeapi.urls', namespace='counteyeapi')),
]
