# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm
from . import views
from .views import AdeiaListView

urlpatterns = [
    path('accounts/login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('accounts/password_change/', views.password_change, name='password_change'),
    
    #acs_employees
    path("acs/adeia", AdeiaListView.as_view(), name="acs-adeies")
]
