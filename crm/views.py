from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CompanyForm, EmployeeForm, TaskForm, CompanyImportForm, EmployeeUpdateForm, ManagerEmployeeUpdateForm
from django.http import HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib import messages
import csv
from django.db import transaction
from .utils import * 
from django.contrib.auth.models import (
    User,
    Group
)
from .models import (
    Company,
    Employee,
    Task
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
    
    if not manager_or_admin(request.user):

        raise PermissionDenied

    if request.method == 'POST':

        form = CompanyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            company = form.save(
                commit=False
            )

            country_code = request.POST.get(
                'country_code',
                '+91'
            )

            company.phone = (
                f'{country_code}{company.phone}'
            )

            company.save()

            return redirect(
                'dashboard'
            )

    else:

        form = CompanyForm()

    return render(
        request,
        'company_form.html',
        {
            'form': form,
            'heading': 'Create Company'
        }
    )



@login_required
def update_company(request, slug):
    
    if not manager_or_admin(request.user):

        raise PermissionDenied

    company = get_object_or_404(
        Company,
        slug=slug
    )
    
    if is_manager(request.user):

        if company.manager != request.user.employee:

            raise PermissionDenied

    if request.method == 'POST':

        form = CompanyForm(
            request.POST,
            request.FILES,
            instance=company
        )

        if form.is_valid():

            form.save()

            return redirect(
                'company_detail',
                slug=company.slug
            )

    else:

        form = CompanyForm(
            instance=company
        )

    return render(
        request,
        'company_form.html',
        {
            'form': form,
            'heading': 'Update Company'
        }
    )
    


@login_required
def delete_company(request, slug):

    if not manager_or_admin(request.user):

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

    return render(
        request,
        'company_confirm_delete.html',
        {
            'company': company
        }
    )



@login_required
def company_list(request):
    
    if is_representative(request.user):
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
            name__icontains=search
        )

    paginator = Paginator(
        companies,
        5
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
def company_detail(request, slug):
    
    if is_representative(request.user):
        raise PermissionDenied

    company = get_object_or_404(
        Company,
        slug=slug
    )
    
    if is_manager(request.user):

        if company.manager != request.user.employee:

            raise PermissionDenied

    return render(
        request,
        'company_detail.html',
        {
            'company': company
        }
    )



@login_required
def create_employee(request):
    
    if not is_admin(request.user):

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
            'heading': 'Create Employee'
        }
    )

    

@login_required
def employee_list(request):

    if is_representative(request.user):
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

    if search:

        employees = employees.filter(
            user__username__icontains=search
        )
    
    paginator = Paginator(
        employees,
        5
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
            'search': search
        }
    )
    

@login_required
def employee_detail(request, id):

    if is_representative(request.user):

        raise PermissionDenied

    employee = get_object_or_404(
        Employee,
        id=id
    )

    if is_manager(request.user):

        if employee.role != 'representative':

            raise PermissionDenied

        if (
            employee.reporting_manager
            != request.user.employee
        ):

            raise PermissionDenied

    return render(
        request,
        'employee_detail.html',
        {
            'employee': employee
        }
    )
    

@login_required
def update_employee(request, id):

    employee = get_object_or_404(
        Employee,
        id=id
    )

    if is_representative(request.user):

        raise PermissionDenied
    
    if is_manager(request.user):

        if (
            employee.role != 'representative'
            or
            employee.reporting_manager
            != request.user.employee
        ):

            raise PermissionDenied

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

            form.save()

            return redirect(
                'employee_detail',
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
            'heading': 'Update Employee'
        }
    )
    

@login_required
def delete_employee(request, id):
    
    employee = get_object_or_404(
        Employee,
        id=id
    )

    if not is_admin(request.user):

        raise PermissionDenied
        
        
    if request.method == 'POST':

        employee.user.delete()

        return redirect(
            'employee_list'
        )

    return render(
        request,
        'employee_confirm_delete.html',
        {
            'employee': employee
        }
    )
    
    
#### TASK ####

@login_required
def create_task(request):
    
    if not manager_or_admin(request.user):

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
        'status'
    )

    priority = request.GET.get(
        'priority'
    )

    if search:

        tasks = tasks.filter(
            title__icontains=search
        )

    if status:

        tasks = tasks.filter(
            status=status
        )

    if priority:

        tasks = tasks.filter(
            priority=priority
        )
        
        
    return render(
        request,
        'task_list.html',
        {
            'tasks': tasks,
            'search': search,
            'status': status,
            'priority': priority,
        }
    )
    
    

@login_required
def task_detail(request, id):

    task = get_object_or_404(
        Task,
        id=id
    )

    if is_representative(request.user):

        if task.employee != request.user.employee:

            raise PermissionDenied

    elif is_manager(request.user):

        if task.employee.reporting_manager != request.user.employee:

            raise PermissionDenied

    return render(
        request,
        'task_detail.html',
        {
            'task': task
        }
    )
    
@login_required
def update_task(request, id):
    
    task = get_object_or_404(
        Task,
        id=id
    )
    
    if is_representative(request.user):

        raise PermissionDenied

    if is_manager(request.user):

        if task.employee.reporting_manager != request.user.employee:

            raise PermissionDenied


    if not manager_or_admin(request.user):

        raise PermissionDenied
        
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
                'task_detail',
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
            'heading': 'Update Task'
        }
    )
    

@login_required
def delete_task(request, id):

    task = get_object_or_404(
        Task,
        id=id
    )
    
    if is_representative(request.user):

        raise PermissionDenied

    if is_manager(request.user):

        if task.employee.reporting_manager != request.user.employee:

            raise PermissionDenied
    

    if not manager_or_admin(request.user):

        raise PermissionDenied

    if request.method == 'POST':

        task.delete()

        return redirect(
            'task_list'
        )

    return render(
        request,
        'task_confirm_delete.html',
        {
            'task': task
        }
    )



@login_required
def export_companies_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="companies.csv"'

    writer = csv.writer(response)

    writer.writerow(
        [
            'Name',
            'Email',
            'Phone',
            'Address'
        ]
    )

    companies = Company.objects.all()

    for company in companies:

        writer.writerow(
            [
                company.name,
                company.email,
                company.phone,
                company.address
            ]
        )

    return response


@login_required
def import_companies_csv(request):

    if not (
        is_admin(request.user)
        or
        is_manager(request.user)
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