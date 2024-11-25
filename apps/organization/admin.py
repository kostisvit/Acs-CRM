from django.contrib import admin
from .models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id','organization_title','organization_title_alias','owner_name','address','city','postal_code','country','phone_number_1','phone_number_2','email','is_active','created','modified')
    list_filter = ('organization_title','owner_name')

admin.site.register(Organization,OrganizationAdmin)
