from django.urls import path
from . import views

app_name = "organizations"

urlpatterns = [
    path("", views.organization_list, name="organization_list"),
    path("import", views.import_customers, name="import_customers")
]
