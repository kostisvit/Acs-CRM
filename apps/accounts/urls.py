# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm
from . import views

urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
