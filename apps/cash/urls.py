from django.urls import path

from .views import customer_list

app_name="cash"

urlpatterns = [
    path("customer/list", customer_list, name="customer_list")
]
