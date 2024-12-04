from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Company,Adeia, Training
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.hashers import make_password
from .forms import UserCreationForm

class CustomUserAdmin(ImportExportModelAdmin):
    model = User
    add_form = UserCreationForm
    list_display = ('id','email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ()
    fieldsets = (
        (None, {'fields': ('email','company')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email',  'is_staff','is_active','phone_number','groups', 'user_permissions')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        """
        Overriding save_model to set a default password for new users.
        """
        if not change:  # This is a new user
            if not obj.password:  # If no password is provided
                default_password = "defaultpassword123"  # Replace with your desired default password
                obj.password = make_password(default_password)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # Include all users, both active and inactive
        return super().get_queryset(request)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','company_title','company_title_alias','company_owner_name','company_address','company_city','company_postal_code','company_country','company_phone_number_1','company_phone_number_2','company_email','company_is_active','created','modified')
    list_filter = ('company_title','company_owner_name')



class AdeiesAdmin(ImportExportModelAdmin):
    date_hierarchy = 'created'
    list_display = ('acs_employee', 'adeiatype', 'startdate','enddate', 'days', 'created')
    search_fields = ['acs_employee']
    list_filter = ['acs_employee', 'created']
    


class TrainingAdmin(ImportExportModelAdmin):
    list_display = ('foreas', 'importdate', 'place', 'training_type', 'app', 'time', 'employee', 'created_at', 'updated_at')
    list_filter = ['employee','foreas','training_type']


admin.site.register(Company,CompanyAdmin)
admin.site.register(User,CustomUserAdmin)
admin.site.register(Adeia, AdeiesAdmin)