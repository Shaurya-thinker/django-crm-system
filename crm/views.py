from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CompanyForm, EmployeeForm, TaskForm, CompanyImportForm, EmployeeUpdateForm, ManagerEmployeeUpdateForm, AccessRoleForm
from django.http import HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib import messages
import csv
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib import messages
from django.db import transaction
from .utils import *
from django.http import JsonResponse
from django.contrib.auth.models import (
    User,
    Group
)
from django.db.models import Q
from .models import (
    Company,
    Employee,
    Task,
    Role,
    Permission,
    RolePermission
)
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.shortcuts import (
    render,
    redirect
)

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)


def custom_403(request, exception):

    return render(
        request,
        '403.html',
        status=403
    )


def custom_404(request, exception):

    return render(
        request,
        '404.html',
        status=404
    )
    

def ajax_validate(request):

    current_id = request.GET.get(
        'current_id'
    )
    
    validation_type = request.GET.get(
        'type'
    )

    value = request.GET.get(
        'value',
        ''
    )

    exists = False

    if validation_type == 'username':

        queryset = User.objects.filter(
            username__iexact=value
        )

        if current_id:

            employee = Employee.objects.filter(
                id=current_id
            ).first()

            if employee:

                queryset = queryset.exclude(
                    id=employee.user.pk
                )

        exists = queryset.exists()

    elif validation_type == 'email':

        queryset = User.objects.filter(
            email__iexact=value
        )

        if current_id:

            employee = Employee.objects.filter(
                id=current_id
            ).first()

            if employee:

                queryset = queryset.exclude(
                    id=employee.user.pk
                )

        exists = queryset.exists()

    elif validation_type == 'company_name':

        queryset = Company.objects.filter(
            name__iexact=value
        )

        if current_id:

            queryset = queryset.exclude(
                id=current_id
            )

        exists = queryset.exists()

    elif validation_type == 'company_email':
        company_queryset = Company.objects.filter(
            email__iexact=value
        )

        if current_id:

            company_queryset = company_queryset.exclude(
                id=current_id
            )

        user_queryset = User.objects.filter(
            email__iexact=value
        )

        exists = (
            company_queryset.exists()
            or
            user_queryset.exists()
        )
        
    elif validation_type == 'phone':
        company_queryset = Company.objects.filter(
            phone=value
        )

        employee_queryset = Employee.objects.filter(
            phone=value
        )

        if current_id:

            company_queryset = company_queryset.exclude(
                id=current_id
            )

            employee_queryset = employee_queryset.exclude(
                id=current_id
            )

        exists = (
            company_queryset.exists()
            or
            employee_queryset.exists()
        )
        
    return JsonResponse(
        {
            'exists': exists
        }
    )


def login_view(request):

    if request.user.is_authenticated:

        return redirect(
            'dashboard'
        )
    

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )
        
        if user and (
            not user.is_superuser
            and
            not hasattr(user, 'employee')
        ):

            logout(request)

            messages.error(
                request,
                'No role assigned to this account.'
            )

            return redirect('login')

        if user:

            login(
                request,
                user
            )

            return redirect(
                'dashboard'
            )

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'login.html'
    )


def logout_view(request):

    logout(request)

    return redirect(
        'login'
    )
    

@login_required
def my_profile(request):

    if request.user.is_superuser:

        if request.user.is_superuser:

            return render(
                request,
                "my_profile.html",
                {
                    "is_admin": True
                }
            )

    return render(
        request,
        'my_profile.html',
        {
            'employee': request.user.employee
        }
    )


class CustomPasswordResetView(
    PasswordResetView
):

    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = '/password-reset/done/'


    def form_valid(self, form):

        last_reset = self.request.session.get(
            'last_password_reset'
        )

        if last_reset:

            last_reset_time = timezone.datetime.fromisoformat(
                last_reset
            )

            if (
                timezone.now()
                <
                last_reset_time + timedelta(seconds=60)
            ):

                remaining = int(
                    (
                        last_reset_time
                        + timedelta(seconds=60)
                        - timezone.now()
                    ).total_seconds()
                )

                messages.error(
                    self.request,
                    f'Please wait {remaining} seconds before requesting another reset email.'
                )

                return self.form_invalid(form)

        self.request.session[
            'last_password_reset'
        ] = timezone.now().isoformat()

        return super().form_valid(form)


class CustomPasswordResetDoneView(
    PasswordResetDoneView
):

    template_name = 'password_reset_done.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

        last_reset = self.request.session.get(
            'last_password_reset'
        )

        remaining = 0

        if last_reset:

            last_reset_time = timezone.datetime.fromisoformat(
                last_reset
            )

            remaining = max(
                0,
                60 - int(
                    (
                        timezone.now()
                        - last_reset_time
                    ).total_seconds()
                )
            )

        context[
            'remaining_seconds'
        ] = remaining

        return context




@login_required
def dashboard(request):

    total_companies = Company.objects.count()

    if (
        is_representative(request.user)
        and hasattr(request.user, 'employee')
    ):

        total_employees = 1

    elif (
        is_manager(request.user)
        and hasattr(request.user, 'employee')
    ):

        total_employees = Employee.objects.filter(
            reporting_manager=request.user.employee
        ).count()

    else:

        total_employees = Employee.objects.count()

    if (
        is_representative(request.user)
        and hasattr(request.user, 'employee')
    ):

        total_tasks = Task.objects.filter(
            employee=request.user.employee
        ).count()

    elif (
        is_manager(request.user)
        and hasattr(request.user, 'employee')
    ):

        total_tasks = Task.objects.filter(
            employee__reporting_manager=request.user.employee
        ).count()

    else:

        total_tasks = Task.objects.count()

    if is_representative(request.user):

        recent_tasks_heading = 'My Recent Tasks'

        recent_tasks = Task.objects.filter(
            employee=request.user.employee
        ).order_by(
            '-created_at'
        )[:5]

    elif is_manager(request.user):

        recent_tasks_heading = (
            'My Team Recent Tasks'
        )

        recent_tasks = Task.objects.filter(
            employee__reporting_manager=request.user.employee
        ).order_by(
            '-created_at'
        )[:5]

    else:

        recent_tasks_heading = (
            'Recent Tasks'
        )

        recent_tasks = Task.objects.order_by(
            '-created_at'
        )[:5]

    return render(
        request,
        'dashboard.html',
        {
            'total_companies': total_companies,
            'total_employees': total_employees,
            'total_tasks': total_tasks,
            'recent_tasks': recent_tasks,
            'recent_tasks_heading': recent_tasks_heading,
        }
    )
    


@login_required
def create_company(request):
    
    if not has_permission(
        request.user,
        "company_create"
    ):

        raise PermissionDenied

    if request.method == 'POST':

        form = CompanyForm(
            request.POST,
            request.FILES,
            user=request.user
        )

        if form.is_valid():

            company = form.save(
                commit=False
            )
            
            if is_manager(request.user):
                company.manager = request.user.employee

            country_code = request.POST.get(
                'country_code',
                '+91'
            )

            company.phone = (
                f'{country_code}{company.phone}'
            )

            company.save()

            return redirect(
                'company_list'
            )

    else:

        form = CompanyForm(
            user=request.user
        )

    return render(
        request,
        'company_form.html',
        {
            'form': form,
            'heading': 'Create Company',
            'current_id': '',
        }
    )



@login_required
def update_company(request, slug):
    
    if not has_permission(
        request.user,
        "company_update"
    ):
        raise PermissionDenied

    company = get_object_or_404(
        Company,
        slug=slug
    )
    
    
    if is_manager(request.user):

        if company.manager != request.user.employee:

            raise PermissionDenied
        
    edit_mode = (
        request.GET.get('edit') == '1'
        or
        request.method == 'POST'
    )
    
    country_code = "+91"

    codes = [
        "+971", "+977", "+880", "+92", "+91", "+86",
        "+82", "+81", "+65", "+61", "+55", "+49",
        "+44", "+39", "+34", "+33", "+27", "+94",
        "+7", "+1"
    ]

    for code in sorted(codes, key=len, reverse=True):
        if company.phone.startswith(code):
            country_code = code
            company.phone = company.phone[len(code):]
            break

    if request.method == 'POST':

        form = CompanyForm(
            request.POST,
            request.FILES,
            instance=company,
            user=request.user
        )

        if form.is_valid():

            company = form.save(commit=False)

            country_code = request.POST.get(
                'country_code',
                '+91'
            )

            company.phone = f'{country_code}{company.phone}'

            company.save()

            return redirect(
                'update_company',
                slug=company.slug
            )

    else:

        form = CompanyForm(
            instance=company,
            user=request.user
        )

    return render(
        request,
        'company_form.html',
        {
            'form': form,
            'heading': 'Update Company',
            'current_id': company.pk,
            'country_code': country_code,
            'company': company,
            'edit_mode': edit_mode,
        }
    )
    


@login_required
def delete_company(request, slug):

    if not has_permission(
        request.user,
        "company_delete"
    ):
        raise PermissionDenied

    company = get_object_or_404(
        Company,
        slug=slug
    )
    
    if is_manager(request.user):

        if company.manager != request.user.employee:

            raise PermissionDenied

    if request.method == 'POST':

        company.delete()

        return redirect(
            'company_list'
        )

    return redirect('company_detail', slug=company.slug)



@login_required
def company_list(request):
    
    if not has_permission(
        request.user,
        "company_view"
    ):
        raise PermissionDenied
   
    if is_manager(request.user):

        companies = Company.objects.filter(
            manager=request.user.employee
        )

    else:

        companies = Company.objects.all()

    search = request.GET.get(
        'search',
        ''
    )

    if search:

        companies = companies.filter(

            Q(name__icontains=search)
            |
            Q(email__icontains=search)
            |
            Q(phone__icontains=search)
            |
            Q(address__icontains=search)

        )

    paginator = Paginator(
        companies,
        10
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        'company_list.html',
        {
            'page_obj': page_obj,
            'search': search
        }
    )



@login_required
def create_employee(request):
    
    if not has_permission(
        request.user,
        "employee_create"
    ):
        raise PermissionDenied

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            with transaction.atomic():

                username = str(
                    form.cleaned_data.get(
                        'username',
                        ''
                    )
                )

                email = form.cleaned_data.get(
                    'email'
                )

                password = form.cleaned_data.get(
                    'password'
                )

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                employee = form.save(
                    commit=False
                )

                employee.user = user

                country_code = request.POST.get(
                    'country_code',
                    '+91'
                )

                employee.phone = (
                    f'{country_code}{employee.phone}'
                )

                employee.save()

                employee_group = Group.objects.get(
                    name='Employee'
                )

                user.groups.add(
                    employee_group
                )

            return redirect(
                'employee_list'
            )

    else:

        form = EmployeeForm()

    return render(
        request,
        'employee_form.html',
        {
            'form': form,
            'heading': 'Create Employee',
            'current_id': '',
        }
    )

    

@login_required
def employee_list(request):

    if not has_permission(
        request.user,
        "employee_view"
    ):
        raise PermissionDenied

    employees = Employee.objects.select_related(
        'user',
    )


    if is_manager(request.user):

        employees = employees.filter(
            role='representative'
        ).select_related(
            'reporting_manager',
            'user',
        )

    search = request.GET.get(
        'search',
        ''
    )
    
    role = request.GET.get(
        'role',
        ''
    )

    access_role = request.GET.get(
        'access_role',
        ''
    )

    if search:

        employees = employees.filter(

            Q(user__username__icontains=search)
            |
            Q(user__email__icontains=search)
            |
            Q(phone__icontains=search)
            |
            Q(access_role__name__icontains=search)
            |
            Q(reporting_manager__user__username__icontains=search)

        )
        
    if role:

        employees = employees.filter(
            role=role
        )

    if access_role:

        employees = employees.filter(
            access_role_id=access_role
        )
        
    access_roles = Role.objects.filter(
        is_active=True
    ).order_by(
        'name'
    )
    
    paginator = Paginator(
        employees,
        10
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        'employee_list.html',
        {
            'page_obj': page_obj,
            'search': search,
            'role': role,
            'access_role': access_role,
            'access_roles': access_roles,
        }
    )
    

@login_required
def update_employee(request, id):

    employee = get_object_or_404(
        Employee,
        id=id
    )

    if not has_permission(
        request.user,
        "employee_update"
    ):
        raise PermissionDenied
    
    if is_manager(request.user):

        if (
            employee.role != 'representative'
            or
            employee.reporting_manager
            != request.user.employee
        ):

            raise PermissionDenied
        
    edit_mode = (
        request.GET.get('edit') == '1'
        or
        request.method == 'POST'
    )
        
    country_code = "+91"

    codes = [
        "+971", "+977", "+880", "+92", "+91", "+86",
        "+82", "+81", "+65", "+61", "+55", "+49",
        "+44", "+39", "+34", "+33", "+27", "+94",
        "+7", "+1"
    ]

    for code in sorted(codes, key=len, reverse=True):

        if employee.phone.startswith(code):

            country_code = code
            employee.phone = employee.phone[len(code):]

            break
    

    if request.method == 'POST':

        if is_admin(request.user):

            form = EmployeeUpdateForm(
                request.POST,
                request.FILES,
                instance=employee
            )

        else:

            form = ManagerEmployeeUpdateForm(
                request.POST,
                request.FILES,
                instance=employee
            )

        if form.is_valid():

            employee = form.save(commit=False)

            country_code = request.POST.get(
                'country_code',
                '+91'
            )

            employee.phone = (
                f'{country_code}{employee.phone}'
            )

            employee.save()

            return redirect(
                'update_employee',
                id=employee.pk
            )

    else:

        if is_admin(request.user):

            form = EmployeeUpdateForm(
                instance=employee
            )

        else:

            form = ManagerEmployeeUpdateForm(
                instance=employee
            )

    return render(
        request,
        'employee_form.html',
        {
            'form': form,
            'heading': 'Update Employee',
            'current_id': employee.pk,
            'country_code': country_code,
            'employee': employee,
            'edit_mode': edit_mode,
        }
    )
    

@login_required
def delete_employee(request, id):
    
    employee = get_object_or_404(
        Employee,
        id=id
    )

    if not has_permission(
        request.user,
        "employee_delete"
    ):
        raise PermissionDenied
        
        
    if request.method == 'POST':

        employee.user.delete()

        return redirect(
            'employee_list'
        )

    return redirect('employee_detail', id=employee.pk)
    
#### TASK ####

@login_required
def create_task(request):
    
    if not has_permission(
        request.user,
        "task_create"
    ):
        raise PermissionDenied

    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            request.FILES,
            user=request.user
        )

        if form.is_valid():

            form.save()

            return redirect(
                'task_list'
            )
        else:
            print(form.errors)
            print(form.non_field_errors())

    else:

        form = TaskForm(
            user=request.user
        )

    return render(
        request,
        'task_form.html',
        {
            'form': form,
            'heading': 'Create Task'
        }
    )
    

@login_required
def task_list(request):
    
    if not has_permission(
        request.user,
        "task_view"
    ):
        raise PermissionDenied

    tasks = Task.objects.select_related(
        'company',
        'employee',
        'employee__user'
    )
    
    if is_representative(request.user):

        tasks = tasks.filter(
            employee=request.user.employee
        )

    elif is_manager(request.user):

        manager = request.user.employee

        tasks = tasks.filter(
            employee__reporting_manager=manager
        )

    search = request.GET.get(
        'search',
        ''
    )

    status = request.GET.get(
        'status',
        ''
    )

    priority = request.GET.get(
        'priority',
        ''
    )

    if search:

        tasks = tasks.filter(
            Q(title__icontains=search)
            |
            Q(description__icontains=search)
            |
            Q(company__name__icontains=search)
            |
            Q(employee__user__username__icontains=search)
        )

    if status:

        tasks = tasks.filter(
            status=status
        )

    if priority:

        tasks = tasks.filter(
            priority=priority
        )
        
    paginator = Paginator(
        tasks,
        10
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        'task_list.html',
        {
            'page_obj': page_obj,
            'search': search,
            'status': status,
            'priority': priority,
        }
    )
    
    
@login_required
def update_task(request, id):
    
    task = get_object_or_404(
        Task,
        id=id
    )
    
    if not has_permission(
        request.user,
        "task_update"
    ):
        raise PermissionDenied

    if is_manager(request.user):

        if task.employee.reporting_manager != request.user.employee:

            raise PermissionDenied
        
    edit_mode = (
        request.GET.get('edit') == '1'
        or
        request.method == 'POST'
    )

        
    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            request.FILES,
            instance=task,
            user=request.user
        )

        if form.is_valid():

            form.save()

            return redirect(
                'update_task',
                id=task.pk
            )

    else:

        form = TaskForm(
            instance=task,
            user=request.user
        )

    return render(
        request,
        'task_form.html',
        {
            'form': form,
            'heading': 'Update Task',
            'task': task,
            'edit_mode': edit_mode,
        }
    )
    

@login_required
def delete_task(request, id):

    task = get_object_or_404(
        Task,
        id=id
    )
    
    if not has_permission(
        request.user,
        "task_delete"
    ):
        raise PermissionDenied

    if is_manager(request.user):

        if task.employee.reporting_manager != request.user.employee:

            raise PermissionDenied
    

    if request.method == 'POST':

        task.delete()

        return redirect(
            'task_list'
        )

    return redirect('task_detail', id=task.pk)



@login_required
def export_companies_csv(request):

    if not has_permission(
        request.user,
        "company_import"
    ):
        raise PermissionDenied

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="companies.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Name',
        'Email',
        'Phone',
        'Address'
    ])

    companies = Company.objects.all()

    for company in companies:

        writer.writerow([
            company.name,
            company.email,
            company.phone,
            company.address
        ])

    return response


@login_required
def import_companies_csv(request):

    if not has_permission(
        request.user,
        "company_import"
    ):
        raise PermissionDenied

    if request.method == 'POST':

        form = CompanyImportForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            csv_file = request.FILES[
                'csv_file'
            ]
            
            if not csv_file.name.endswith(
                '.csv'
            ):
                messages.error(
                    request,
                    'Please upload a CSV file.'
                )

                return redirect(
                    'import_companies_csv'
                )

            decoded_file = csv_file.read().decode(
                'utf-8'
            )

            reader = csv.reader(
                decoded_file.splitlines()
            )

            next(reader)

            created_count = 0
            skipped_count = 0

            for row in reader:
                if not row:
                    continue
                if len(row) < 4:

                    skipped_count += 1

                    continue
                name = row[0]
                email = row[1]
                phone = row[2]
                address = row[3]

                if Company.objects.filter(
                    name=name
                ).exists():

                    skipped_count += 1

                    continue

                Company.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    address=address
                )

                created_count += 1

            messages.success(
                request,
                f'Import Complete! Created: {created_count}, Skipped: {skipped_count}'
            )

            return redirect(
                'company_list'
            )

    else:

        form = CompanyImportForm()

    return render(
        request,
        'import_companies.html',
        {
            'form': form
        }
    )
    
    

@login_required
def download_company_template(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="company_template.csv"'
    )

    writer = csv.writer(
        response
    )

    writer.writerow(
        [
            'Name',
            'Email',
            'Phone',
            'Address'
        ]
    )

    writer.writerow(
        [
            'Google',
            'contact@google.com',
            '1234567890',
            'California, USA'
        ]
    )

    writer.writerow(
        [
            'Microsoft',
            'contact@microsoft.com',
            '9876543210',
            'Washington, USA'
        ]
    )

    return response




@login_required
def access_role_list(request):

    if not is_admin(request.user):
        raise PermissionDenied

    roles = Role.objects.order_by(
        "name"
    )

    return render(
        request,
        "access_role_list.html",
        {
            "roles": roles
        }
    )
    


@login_required
def create_access_role(request):

    if not is_admin(request.user):

        raise PermissionDenied

    if request.method == "POST":

        form = AccessRoleForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("access_role_list")

    else:

        form = AccessRoleForm()

    return render(
        request,
        "access_role_form.html",
        {
            "form": form,
            "heading": "Create Access Role",
            "current_id": "",
        },
    )
    

@login_required
def update_access_role(request, id):

    if not is_admin(request.user):

        raise PermissionDenied

    role = get_object_or_404(
        Role,
        id=id,
    )

    if request.method == "POST":

        form = AccessRoleForm(
            request.POST,
            instance=role,
        )

        if form.is_valid():

            form.save()

            return redirect("access_role_list")

    else:

        form = AccessRoleForm(
            instance=role,
        )

    return render(
        request,
        "access_role_form.html",
        {
            "form": form,
            "heading": "Update Access Role",
            "current_id": role.pk,
        },
    )
    

@login_required
def manage_role_permissions(request, id):

    if not is_admin(request.user):

        raise PermissionDenied

    role = get_object_or_404(
        Role,
        id=id
    )

    permissions = Permission.objects.all().order_by(
        "module",
        "name"
    )

    assigned_permissions = RolePermission.objects.filter(
        role=role
    ).values_list(
        "permission_id",
        flat=True
    )
    
    if request.method == "POST":

        selected_permissions = request.POST.getlist(
            "permissions"
        )

        RolePermission.objects.filter(
            role=role
        ).delete()

        role_permissions = [

            RolePermission(
                role=role,
                permission_id=permission_id
            )

            for permission_id in selected_permissions
        ]

        RolePermission.objects.bulk_create(
            role_permissions
        )

        messages.success(
            request,
            "Permissions updated successfully."
        )

        return redirect(
            "manage_role_permissions",
            id=role.pk
        )

    return render(
        request,
        "manage_role_permissions.html",
        {
            "role": role,
            "permissions": permissions,
            "assigned_permissions": assigned_permissions,
        }
    )