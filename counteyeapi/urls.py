from django.urls import path
from .views import CountList, CountDetail, CreateCount, EditCount, DeleteCount, AdminCountDetail
from rest_framework.routers import DefaultRouter

app_name = 'counteyeapi'

# router = DefaultRouter()
# router.register('', CountList, basename='post')
# urlpatterns = router.urls

# urlpatterns = [
#     path('<int:pk>/', CountDetail.as_view(), name='detailcreate'), 
#     path('', CountList.as_view(), name='listcreate'),
# ]

urlpatterns = [
    path('', CountList.as_view(), name='countlist'),
    path('post/<str:pk>/', CountDetail.as_view(), name='detailcount'),
    # Post Admin URLs
    path('admin/create/', CreateCount.as_view(), name='createcount'),
    path('admin/edit/countdetail/<int:pk>/', AdminCountDetail.as_view(), name='admindetailcount'),
    path('admin/edit/<int:pk>/', EditCount.as_view(), name='editcount'),
    path('admin/delete/<int:pk>/', DeleteCount.as_view(), name='deletecount'),
]