# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm
from . import views
from .views import adeia_list,AcsProfile

urlpatterns = [
    path('accounts/login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('accounts/password_change/', views.password_change, name='password_change'),
    path('accounts/update-profile/', views.update_profile, name='update_profile'),
    
    #acs_employees
    path("acs/adeia", views.adeia_list, name="acs-adeies"),
    path("acs/user/profile", AcsProfile.as_view(), name="profile")
]
