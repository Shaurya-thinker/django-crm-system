from django.contrib import admin
from .models import Company, Employee, Task


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
        'company',
        'designation',
        'phone'
    )

    search_fields = (
        'user__username',
        'user__email',
        'designation'
    )

    list_filter = (
        'role',
        'company'
    )
    
    

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'employee',
        'status',
        'priority',
        'deadline',
        'created_at'
    )

    search_fields = (
        'title',
        'employee__user__username'
    )

    list_filter = (
        'status',
        'priority'
    )