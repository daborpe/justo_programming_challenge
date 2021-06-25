from django.urls import path
from .views import HitList, HitCreate, HitUpdate, HitListBulk

app_name = 'hits'

urlpatterns = [
    path('hits/', HitList.as_view(), name='list'),
    path('hits/bulk/', HitListBulk.as_view(), name='bulk'),
    path('hits/create/', HitCreate.as_view(), name='create'),
    path('hits/<int:pk>/', HitUpdate.as_view(), name='update'),
]
