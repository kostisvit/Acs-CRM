from django.urls import path
from . import views

app_name = "parameters"

urlpatterns = [
        path(
        "import/customers/",
        views.import_csv,
        {"import_type": "customers"},
        name="import_customers",
    ),
]