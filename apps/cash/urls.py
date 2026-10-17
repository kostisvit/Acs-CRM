from django.urls import path

from .views import customer_list

urlpatterns = [
    path("customer/list", customer_list, name="customer_list")
]
