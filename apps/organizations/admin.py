from django.contrib import admin
from .models import Organization, Employee, Tasks


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["org_name", "org_address", "org_city", "org_phone","source_id"]
    search_fields = ["org_name", "org_address", "org_city"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["organization", "firstname", "lastname","phone","cellphone","email","secondary_email","is_active","org_department","source_id"]
    search_fields = ["organization","lastname"]
    list_filter = ["is_active", "org_department", "organization"]

    def delete_queryset(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['organization','importdate','org_app','job_type_acs','acs_employee','task_time','org_employee','created','modified']
    search_fields = ["organization","task_info"]
    list_filter = ["organization", "acs_employee"]