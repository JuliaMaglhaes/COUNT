from django.urls import path
from .views import CountList, CountDetail

app_name = 'counteyeapi'

urlpatterns = [
    path('<int:pk>/', CountDetail.as_view(), name='detailcreate'), 
    path('', CountList.as_view(), name='listcreate'),
]