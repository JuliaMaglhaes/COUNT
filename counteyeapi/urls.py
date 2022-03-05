from django.urls import path,  re_path
from .views import CountList, CountDetail, CreateCount, EditCount, DeleteCount, AdminCountDetail
from rest_framework.routers import DefaultRouter
from .import views

app_name = 'counteyeapi'

# router = DefaultRouter()
# router.register('', CountList, basename='post')
# urlpatterns = router.urls

urlpatterns = [
    path('', CountList.as_view(), name='countlist'),
    path('post/<str:pk>/', CountDetail.as_view(), name='detailcount'),
    path('admin/create/', CreateCount.as_view(), name='createcount'),
    path('admin/edit/countdetail/<int:pk>/', AdminCountDetail.as_view(), name='admindetailcount'),
    path('admin/edit/<int:pk>/', EditCount.as_view(), name='editcount'),
    path('admin/delete/<int:pk>/', DeleteCount.as_view(), name='deletecount'),
    re_path(r'^(?P<stream_path>(.*?))/$',views.dynamic_stream,name="videostream"),  
    re_path(r'^stream/$',views.indexscreen)
]