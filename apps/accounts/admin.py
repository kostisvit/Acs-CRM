from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.hashers import make_password
from .forms import UserCreationForm

class CustomUserAdmin(ImportExportModelAdmin):

    

    model = User
    add_form = UserCreationForm
    list_display = ('id','email', 'first_name', 'last_name', 'is_staff', 'is_active','gender','is_company_owner')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('organization','first_name', 'last_name', 'date_of_birth','phone_number','postal_code','address','city','country','gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_company_owner','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('organization','first_name', 'last_name', 'email',  'is_staff','is_active','is_company_owner','date_of_birth','phone_number','address','city','country','gender','postal_code','groups', 'user_permissions')}
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


admin.site.register(User,CustomUserAdmin)