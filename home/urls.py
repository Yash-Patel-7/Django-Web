from os import name
from . import views
from django.urls import path


app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('verified/<str:url>/', views.verified, name='verified'),
    path('login/', views.login, name='login'),
    path('OTPP/', views.OTPP, name='OTPP'),
    path('notification-verify-email/', views.notif_verify_email, name='notif_verify_email'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]

