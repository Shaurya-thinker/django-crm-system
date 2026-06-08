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
        'company',
        'designation'
    )

    search_fields = (
        'user__username',
        'designation'
    )
    
    

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'employee',
        'status',
        'priority',
        'deadline'
    )

    search_fields = (
        'title',
        'employee__user__username'
    )

    list_filter = (
        'status',
        'priority'
    )