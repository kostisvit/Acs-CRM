from django.contrib import admin
from .models import JobType, OrgDepartment, TrainingType, TrainingPlace, OtsSoftware


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created", "modified")
    list_filter = ("is_active",)
    search_fields = ("name",)
  
@admin.register(OrgDepartment)
class OrgDepartmentAdmin(admin.ModelAdmin): 
    list_display = ("name", "is_active", "created", "modified")
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created", "modified")
    list_filter = ("is_active",)
    search_fields = ("name",)
  
@admin.register(TrainingPlace)
class TrainingPlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created", "modified")
    list_filter = ("is_active",)
    search_fields = ("name",)
    
@admin.register(OtsSoftware)
class OtsSoftwareAdmin(admin.ModelAdmin): 
    list_display = ("name", "is_active", "created", "modified")
    list_filter = ("is_active",)
    search_fields = ("name",) 
