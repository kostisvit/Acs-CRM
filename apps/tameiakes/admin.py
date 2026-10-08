from django.contrib import admin

from .models import Cash, Customer


@admin.action(description="Selected cash estiasi as True")
def make_cash_estiasi_is_true(modeladmin, request, queryset):
    queryset.update(cash_estiasi=True)


@admin.action(description="Selected cash estiasi False")
def make_cash_estiasi_is_false(modeladmin, request, queryset):
    queryset.update(cash_estiasi=False)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "company_name",
        "company_type",
        "company_address",
        "company_email",
        "company_afm",
        "phone",
        "is_active",
        "created",
        "modified",
    )
    search_fields = (
        "first_name",
        "last_name",
        "company_name",
        "company_type",
        "company_address",
        "company_email",
        "phone",
    )
    list_filter = ["is_active"]
    ordering = ("company_name",)



@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "cash_model",
        "cash_number",
        "register_date",
        "current_os",
        "aes_key",
        "is_active",
        "voucher",
        "iris_connect",
        "pos_connect",
        "cash_estiasi",
        "info",
        "created",
        "modified",
    )
    list_filter = ["is_active", "voucher", "iris_connect", "pos_connect", "cash_estiasi"]
    search_fields = ("customer__first_name", "customer__last_name", "description")
    ordering = ("-created",)
    actions = [make_cash_estiasi_is_true, make_cash_estiasi_is_false]



