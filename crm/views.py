from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CompanyForm, EmployeeForm, TaskForm
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

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


def is_admin(user):

    return user.groups.filter(
        name='Admin'
    ).exists()


def is_manager(user):

    return user.groups.filter(
        name='Manager'
    ).exists()


def is_employee(user):

    return user.groups.filter(
        name='Employee'
    ).exists()


def manager_or_admin(user):

    return (
        is_admin(user)
        or
        is_manager(user)
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

        if user:

            login(
                request,
                user
            )

            return redirect(
                'dashboard'
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

    total_employees = Employee.objects.count()

    total_tasks = Task.objects.count()

    if is_employee(request.user):

        recent_tasks_heading = 'My Recent Tasks'

        recent_tasks = Task.objects.filter(
            employee=request.user.employee
        ).order_by(
            '-created_at'
        )[:5]

    else:

        recent_tasks_heading = 'Recent Tasks'

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

            form.save()

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

    companies = Company.objects.all()

    search = request.GET.get(
        'search'
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

    company = get_object_or_404(
        Company,
        slug=slug
    )

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

            form.save()

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

    employees = Employee.objects.select_related(
        'user',
        'company'
    )

    search = request.GET.get(
        'search'
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

    employee = get_object_or_404(
        Employee,
        id=id
    )

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

    if not is_admin(request.user):

        raise PermissionDenied

    if request.method == 'POST':

        form = EmployeeForm(
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

        form = EmployeeForm(
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

        employee.delete()

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
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                'task_list'
            )

    else:

        form = TaskForm()

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
        'employee',
        'employee__user',
        'employee__company'
    )
    
    if is_employee(request.user):

        tasks = tasks.filter(
            employee=request.user.employee
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

    if not manager_or_admin(request.user):

        raise PermissionDenied
        
    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            request.FILES,
            instance=task
        )

        if form.is_valid():

            form.save()

            return redirect(
                'task_detail',
                id=task.pk
            )

    else:

        form = TaskForm(
            instance=task
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