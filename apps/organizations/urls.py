from django.urls import path
from . import views
from .views import OrganizationUpdateView, EmployeeUpdateView, OrganizationCreateView, EmployeeCreateView

app_name = "organizations"

urlpatterns = [
    path("list/", views.organization_list, name="organization_list"),
    path("create/", OrganizationCreateView.as_view(),
         name="organization_create"),
    path("detail/<uuid:pk>/", OrganizationUpdateView.as_view(),
         name="organization_update"),
    path("soft-delete/<uuid:pk>", views.soft_delete_organization,
         name="soft_delete_organization"),
    path("restore/<uuid:pk>", views.restore_organization,
         name="restore_organization"),
    path("employee/list", views.employee_list, name="employee_list"),
    path("employee/create/", EmployeeCreateView.as_view(),
         name="employee_create"),
    path("employee/detail/<uuid:pk>/",
         EmployeeUpdateView.as_view(), name="employee_update"),
    path("employee/soft-delete/<uuid:pk>",
         views.soft_delete_employee, name="soft_delete_employee"),
    path("employee/restore/<uuid:pk>",
         views.restore_employee, name="restore_employee"),
    path("task/list", views.task_list, name="task_list"),
    path("task/create/", views.TaskCreateView.as_view(), name="task_create"),

    path(
        "load-employees/",
        views.load_employees,
        name="load_employees"
    ),


]
