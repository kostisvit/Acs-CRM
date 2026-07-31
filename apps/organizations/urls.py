from django.urls import path
from . import views
from .views import OrganizationUpdateView

app_name = "organizations"

urlpatterns = [
    path("list/", views.organization_list, name="organization_list"),
    path("detail/<uuid:pk>/", OrganizationUpdateView.as_view(), name="organization_update"),
    path("soft-delete/<uuid:pk>", views.soft_delete_organization, name="soft_delete_organization"),
    path("restore/<uuid:pk>", views.restore_organization, name="restore_organization"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employee/soft-delete/<uuid:pk>", views.soft_delete_employee, name="soft_delete_employee"),
    path("employee/restore/<uuid:pk>", views.restore_employee, name="restore_employee"),
    path("task/list", views.task_list, name="task_list"),
    
    
]
