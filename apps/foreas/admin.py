from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from .models import *

class DhmosAdmin(ImportExportModelAdmin):
    list_display = ('id','name', 'phone', 'address', 'city', 'teamviewer', 'fax', 'email', 'is_visible')
    list_filter = ['is_visible']
    list_editable = ['is_visible']
    search_fields = ['name', ]
    actions = ['restore_selected', 'soft_delete_selected']
    history_list_display = ["changed_fields","list_changes"]

    def get_queryset(self, request):
        """
        Override get_queryset to include all records (even soft-deleted ones).
        """
        return Dhmos.all_objects.all()

    def restore_selected(self, request, queryset):
        """
        Action to restore selected soft-deleted dhmoi.
        """
        for obj in queryset:
            obj.restore()
        self.message_user(request, f"{queryset.count()} Δήμος(s) restored.")

    restore_selected.short_description = "Ενεργοποίηση επιλεγμένων Φορέων"

    def soft_delete_selected(self, request, queryset):
        """
        Action to soft-delete selected dhmoi.
        """
        for obj in queryset:
            obj.delete()
        self.message_user(request, f"{queryset.count()} Δήμος(s) soft-deleted.")

    soft_delete_selected.short_description = "Απενεργοποίηση επιλεγμένων Φορέων"



class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('dhmos', 'lastname', 'firstname','tmhma', 'phone', 'email', 'is_visible')
    list_filter = ['is_visible', 'tmhma', 'dhmos']
    search_fields = ['lastname']
    actions = ['make_visible', 'make_unvisible']

    def make_visible(modeladmin, request, queryset):
        queryset.update(is_visible=True)
    make_visible.short_description = "Ενεργοποίηση υπαλλήλου"

    def make_unvisible(modeladmin, request, queryset):
        queryset.update(is_visible=False)
    make_unvisible.short_description = "Απενεργοποίηση υπαλλήλου"

admin.site.register(Dhmos, DhmosAdmin)
admin.site.register(Employee, EmployeeAdmin)




# admin.site.unregister(Group)
admin.site.site_header = "Μαζιώτης Σταύρος & ΣΙΑ ΕΕ"
admin.site.site_title = "Μαζιώτης Σταύρος & ΣΙΑ ΕΕ"
admin.site.index_title = "ACS Services"