from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    ManagerUserList,
    ManagerUserUpdate,
)

app_name = 'users'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('hitmen/', ManagerUserList.as_view(), name='list'),
    path('hitmen/<uuid:pk>/', ManagerUserUpdate.as_view(), name='update'),

]
