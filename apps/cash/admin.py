from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ["name","vat_number","phone","email","address","notes","is_active","created","modified"]
    search_fields = ["name","vat_number"]
    list_filter = ["is_active"]



