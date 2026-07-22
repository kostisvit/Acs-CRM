from django.urls import path
from . import views

app_name = "parameters"

urlpatterns = [
  path("import-data/",views.import_csv,name="import",)
]