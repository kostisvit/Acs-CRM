from django.urls import path

from .views import cash_list, customer_list

app_name="cash"

urlpatterns = [
    path("customer/list", customer_list, name="customer_list"),
    path("cash/list", cash_list, name="cash_list")
]
