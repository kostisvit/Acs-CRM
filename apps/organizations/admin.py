from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["org_name", "org_address", "org_city", "org_phone"]
    search_fields = ["org_name", "org_address", "org_city"]


# Register your models here.
