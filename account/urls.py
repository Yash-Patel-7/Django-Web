from os import name
from . import views
from django.urls import path


app_name = 'account'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reset-password/<str:url>/', views.reset_password, name='reset_password'),
    path('admin/', views.admin, name='admin'),
]

