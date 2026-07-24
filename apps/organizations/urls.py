from django.urls import path
from . import views
from .views import OrganizationUpdateView

app_name = "organizations"

urlpatterns = [
    path("", views.organization_list, name="organization_list"),
    path("<int:pk>/", OrganizationUpdateView.as_view(), name="organization_update"),
    path("organization-delete/<int:pk>", views.soft_delete_organization, name="soft_delete_organization"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employee-delete/<int:pk>", views.soft_delete_employee, name="soft_delete_employee"),
    
]
