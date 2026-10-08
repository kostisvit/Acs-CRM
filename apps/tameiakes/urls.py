from django.urls import path

from . import views

app_name="tameiakes"

urlpatterns = [
    path("list/", views.customer_list, name='customer_list')

]
