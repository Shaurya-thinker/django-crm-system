from django.contrib import admin
from .models import Company, Employee, Task, Role, Permission, RolePermission



admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'phone',
        'created_at'
    )

    search_fields = (
        'name',
        'email'
    )

    prepopulated_fields = {
        'slug': (
            'name',
        )
    }
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role',
        'reporting_manager',
        'access_role',
        'phone'
    )

    search_fields = (
        'user__username',
        'user__email',
        'access_role'
    )

    list_filter = (
        'role',
    )
    
    

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'company',
        'employee',
        'status',
        'priority',
        'deadline',
        'created_at'
    )

    search_fields = (
        'title',
        'company__name',
        'employee__user__username'
    )

    list_filter = (
        'status',
        'priority'
    )