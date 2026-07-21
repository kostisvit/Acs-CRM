from django.urls import path
from . import views
from .views import OrganizationUpdateView

app_name = "organizations"

urlpatterns = [
    path("", views.organization_list, name="organization_list"),
    path("<int:pk>/", OrganizationUpdateView.as_view(), name="organization_detail"),
    path("import", views.import_customers, name="import_customers")
]
