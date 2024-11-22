# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm
from . import views

urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('accounts/password_change/', views.password_change, name='password_change'),
]
