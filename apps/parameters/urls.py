from django.urls import path
from . import views

app_name = "parameters"

urlpatterns = [
  path("", views.parameters_view, name="parameters"),
  path("job-types/", views.jobtype_view, name="job_types"),
  path("job-types/add/", views.add_job_type, name="add_job_type"),
  path("ots-software/", views.ots_software_view, name="ots_software"),
  path("organization-departments", views.org_department_view, name="org_department"),
  path("import-data/",views.import_csv,name="import",)
]