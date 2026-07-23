from django.contrib import admin
from .models import Organization, Employee


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["org_name", "org_address", "org_city", "org_phone","source_id"]
    search_fields = ["org_name", "org_address", "org_city"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["organization", "firstname", "lastname","phone","cellphone","email","secondary_email","is_active","org_department"]
    search_fields = ["organization","lastname"]
    list_filter = ["is_active", "org_department", "organization"]

