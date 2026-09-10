from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin

from .models import Employee, Organization, Task, Training


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["org_name", "org_address",
                    "org_city", "org_phone", "source_id"]
    search_fields = ["org_name", "org_address", "org_city"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["organization", "firstname", "lastname", "phone", "mobile",
                    "email", "secondary_email", "is_active", "org_department", "source_id"]
    search_fields = ["organization", "lastname"]
    list_filter = ["is_active", "org_department", "organization"]

    def delete_queryset(self, request, queryset):
        queryset.update(is_active=False)


class TaskResource(resources.ModelResource):
    organization = fields.Field(
        column_name="organization",
        attribute="organization__org_name",
    )
    org_app = fields.Field(
        column_name="org_app",
        attribute="org_app__name"
    )
    job_type_acs = fields.Field(
        column_name="job_type_acs",
        attribute="job_type_acs__name"
    )
    org_employee = fields.Field(
        column_name="org_employee",
    )

    def dehydrate_acs_employee(self, task):
        if task.acs_employee:
            return f"{task.acs_employee.last_name or ''} {task.acs_employee.first_name or ''}".strip()
        return ""


    def dehydrate_org_employee(self, task):
        if task.org_employee:
            return f"{task.org_employee.lastname or ''} {task.org_employee.firstname or ''}".strip()
        return ""

    class Meta:
        model = Task
        fields = (
            "organization",
            "importdate",
            "org_app",
            "job_type_acs",
            "acs_employee",
            "task_time",
            "org_employee",
            "created",
            "modified",
        )


class TaskAdmin(ImportExportModelAdmin):
    resource_class = TaskResource
    date_hierarchy = "importdate"
    list_display = ['organization', 'importdate', 'org_app', 'job_type_acs',
                    'acs_employee', 'task_time', 'org_employee', 'created', 'modified']
    search_fields = ["organization", "task_info"]
    list_filter = ["organization", "acs_employee"]


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['organization', 'training_date', 'training_type', 'org_app',
                    'acs_employee', 'training_info', 'training_note', 'created', 'modified']
    search_fields = ["organization", "training_info"]
    list_filter = ["organization", "acs_employee"]



admin.site.register(Task, TaskAdmin)
