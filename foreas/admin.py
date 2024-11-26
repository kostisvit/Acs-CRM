from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from .models import *

class DhmosAdmin(ImportExportModelAdmin):
    list_display = ('id','name', 'phone', 'address', 'city', 'teamviewer', 'fax', 'email', 'is_visible')
    list_filter = ['name', 'is_visible']
    list_editable = ['is_visible']
    search_fields = ['name', ]
    actions = ['make_visible', 'make_unvisible']
    history_list_display = ["changed_fields","list_changes"]

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    def list_changes(self, obj):
        fields = ""
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)

            for change in delta.changes:
                fields += str("<strong>{}</strong> changed from <span style='background-color:#ff6347'>{}</span> to <span style='background-color:#009933; font-weight:bold;'>{}</span> . <br/>".format(change.field, change.old, change.new))
            return format_html(fields)
        return None

    def make_visible(modeladmin, request, queryset):
        queryset.update(is_visible=True)
    make_visible.short_description = "Ενεργοποίηση πελάτη"

    def make_unvisible(modeladmin, request, queryset):
        queryset.update(is_visible=False)
    make_unvisible.short_description = "Απενεργοποίηση πελάτη"



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