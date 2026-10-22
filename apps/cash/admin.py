from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import CashRegister, CashRegisterModel, Customer, SoftwareVersion


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ["name","vat_number","company_title","phone","email","address","notes","is_active","created","modified"]
    search_fields = ["name","vat_number"]
    list_filter = ["is_active"]



@admin.register(CashRegisterModel)
class CashRegisterModelAdmin(ImportExportModelAdmin):
    list_display = ["manufacturer","name","description","created","modified"]
    search_fields = ["manufacturer","name"]
    list_filter = ["manufacturer","name"]


@admin.register(SoftwareVersion)
class SoftwareVersionAdmin(ImportExportModelAdmin):
    list_display = ["version_number","release_date","display_compatible_models","release_notes","is_active","created","modified"]
    search_fields = ["version_number","display_compatible_models"]
    list_filter = ["version_number","is_active"]

    @admin.display(description="Συμβατά μοντέλα")
    def display_compatible_models(self, obj):
        return ", ".join(
            str(model)
            for model in obj.compatible_models.all()
        )


@admin.register(CashRegister)
class CashRegisterAdmin(ImportExportModelAdmin):
    list_display = ["customer","model","serial_number","current_version","installation_date","cash_estiasi","status","created","modified"]
    search_fields = ["customer","serial_number","model"]
    list_filter = ["model","cash_estiasi","status"]
