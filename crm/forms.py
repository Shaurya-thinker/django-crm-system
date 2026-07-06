from django import forms
from .models import Company, Employee, Task, Role
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from .utils import *

class CompanyForm(forms.ModelForm):

    class Meta:

        model = Company

        fields = [
            'name',
            'manager',
            'assignee',
            'email',
            'phone',
            'address',
            'logo'
        ]
        widgets = {
            'address': forms.Textarea(
                attrs={
                    'rows': 4
                }
            )
        }
        
    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop(
            'user',
            None
        )

        super().__init__(*args, **kwargs)
        
        manager_queryset = Employee.objects.filter(
            role='manager'
        )

        if self.user and is_admin(self.user):

            # Initial Create page
            assignee_queryset = Employee.objects.none()

            # Form submitted (POST)
            if self.data.get("manager"):

                assignee_queryset = Employee.objects.filter(
                    role="representative",
                    reporting_manager_id=self.data.get("manager"),
                )

            # Update page
            elif self.instance.pk and self.instance.manager:

                assignee_queryset = Employee.objects.filter(
                    role="representative",
                    reporting_manager=self.instance.manager,
                )

        else:

            assignee_queryset = Employee.objects.filter(
                role="representative"
            )

        if self.user and hasattr(self.user, 'employee'):

            if self.user.employee.role == 'manager':

                manager_queryset = manager_queryset.filter(
                    pk=self.user.employee.pk
                )

                assignee_queryset = assignee_queryset.filter(
                    reporting_manager=self.user.employee
                )

        self.fields['manager'].queryset = manager_queryset

        if self.user and hasattr(self.user, 'employee'):

            if self.user.employee.role == 'manager':

                self.fields['manager'].initial = self.user.employee
                self.fields['manager'].disabled = True

        self.fields['assignee'].queryset = assignee_queryset

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    'class': 'form-control'
                }
            )
    
    def clean_phone(self):

        phone = self.cleaned_data.get(
            'phone'
        )

        # Guard against None or empty values before calling string methods
        if not phone:
            raise forms.ValidationError(
                'Phone number is required.'
            )

        # Ensure phone is a string for .isdigit() and length checks
        phone_str = str(phone)

        if not phone_str.isdigit():
            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )

        if len(phone_str) != 10:
            raise forms.ValidationError(
                'Phone number must be exactly 10 digits.'
            )

        return phone_str
    
    def clean(self):

        cleaned_data = super().clean()

        manager = cleaned_data.get(
            'manager'
        )

        assignee = cleaned_data.get(
            'assignee'
        )

        if assignee and manager:

            if assignee.reporting_manager != manager:

                raise forms.ValidationError(
                    'Selected assignee does not report to the selected manager.'
                )

        return cleaned_data


class EmployeeForm(forms.ModelForm):
    
    username = forms.CharField()

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:

        model = Employee

        fields = [
            'role',
            "access_role",
            'reporting_manager',
            'phone',
            'profile_image'
        ]
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields[
            'reporting_manager'
        ].queryset = Employee.objects.filter(
            role='manager'
        )

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    'class': 'form-control'
                }
            )
            
    def clean_phone(self):

        phone = self.cleaned_data.get(
            'phone'
        )

        if not phone:
            raise forms.ValidationError(
                'Phone number is required.'
            )

        phone_str = str(phone)

        if not phone_str.isdigit():

            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )

        if len(phone_str) != 10:

            raise forms.ValidationError(
                'Phone number must be exactly 10 digits.'
            )

        return phone_str
    
    
    def clean(self):

        cleaned_data = super().clean()

        role = cleaned_data.get(
            'role'
        )

        manager = cleaned_data.get(
            'reporting_manager'
        )

        if role == 'manager':

            cleaned_data['reporting_manager'] = None


        if role == 'representative':

            if not manager:

                raise forms.ValidationError(
                    'Representative must have a reporting manager.'
                )

            if manager.representatives.count() >= 5:

                raise forms.ValidationError(
                    'Manager can have maximum 5 representatives.'
                )

        return cleaned_data
    
    def clean_username(self):

        username = self.cleaned_data.get(
            'username'
        )

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                'Username already exists.'
            )

        return username
    
    def clean_email(self):

        email = self.cleaned_data.get(
            'email'
        )

        if User.objects.filter(
            email=email
        ).exists():

            raise forms.ValidationError(
                'Email already exists.'
            )

        return email
    


class EmployeeUpdateForm(forms.ModelForm):

    class Meta:

        model = Employee

        fields = [
            'role',
            "access_role",
            'reporting_manager',
            'phone',
            'profile_image'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields[
            'reporting_manager'
        ].queryset = Employee.objects.filter(
            role='manager'
        )

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    'class': 'form-control'
                }
            )

    def clean_phone(self):

        phone = self.cleaned_data.get(
            'phone'
        )

        if not phone:
            raise forms.ValidationError(
                'Phone number is required.'
            )

        phone_str = str(phone)

        if not phone_str.isdigit():

            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )

        if len(phone_str) != 10:

            raise forms.ValidationError(
                'Phone number must be exactly 10 digits.'
            )

        return phone_str

    def clean(self):

        cleaned_data = super().clean()

        role = cleaned_data.get(
            'role'
        )

        manager = cleaned_data.get(
            'reporting_manager'
        )
        
        if role == 'manager':

            cleaned_data['reporting_manager'] = None
            
        if (
            self.instance.role == 'manager'
            and role != 'manager'
            and self.instance.representatives.exists()
        ):
            raise forms.ValidationError(
                'Cannot change role while representatives are assigned.'
            )

        if role == 'representative':

            if not manager:

                raise forms.ValidationError(
                    'Representative must have a reporting manager.'
                )

            if (
                manager.representatives.count() >= 5
                and manager != self.instance.reporting_manager
            ):

                raise forms.ValidationError(
                    'Manager can have maximum 5 representatives.'
                )

        return cleaned_data


class ManagerEmployeeUpdateForm(forms.ModelForm):

    class Meta:

        model = Employee

        fields = [
            'phone',
            'profile_image'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    'class': 'form-control'
                }
            )

    def clean_phone(self):

        phone = self.cleaned_data.get(
            'phone'
        )

        if not phone:
            raise forms.ValidationError(
                'Phone number is required.'
            )

        phone_str = str(phone)

        if not phone_str.isdigit():

            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )

        if len(phone_str) != 10:

            raise forms.ValidationError(
                'Phone number must be exactly 10 digits.'
            )

        return phone_str

    
class TaskForm(forms.ModelForm):
    
    manager = forms.ModelChoiceField(
        queryset=Employee.objects.filter(
            role='manager'
        ),
        required=False
    )

    class Meta:

        model = Task

        fields = [
            'title',
            'description',
            'manager',
            'company',
            'employee',
            'status',
            'priority',
            'deadline',
            'attachment'
        ]

        widgets = {
            'description': CKEditorWidget(
                config_name='default'
            ),
            'deadline': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):

        user = kwargs.pop(
            'user',
            None
        )
        # keep user on the form instance for use in clean methods
        self.user = user
        super().__init__(
            *args,
            **kwargs
        )
        
        if self.instance.pk and self.instance.company:

            self.fields["manager"].initial = self.instance.company.manager
            
        
        if user and is_admin(user):

            self.fields['employee'].queryset = Employee.objects.none()
            self.fields['company'].queryset = Company.objects.none()

            if self.data.get('manager'):
                manager_id = self.data.get('manager')

                self.fields['employee'].queryset = Employee.objects.filter(
                    role='representative',
                    reporting_manager_id=manager_id
                )

                self.fields['company'].queryset = Company.objects.filter(
                    manager_id=manager_id
                )

            elif self.instance.pk and self.instance.company:
                manager = self.instance.company.manager

                self.fields['manager'].initial = manager

                self.fields['company'].queryset = Company.objects.filter(
                    manager=manager
                )

                self.fields['employee'].queryset = Employee.objects.filter(
                    role='representative',
                    reporting_manager=manager
                )

        elif user and is_manager(user):

                self.fields[
                    'company'
                ].queryset = Company.objects.filter(
                    manager=user.employee
                )

                self.fields[
                    'employee'
                ].queryset = Employee.objects.filter(
                    role='representative',
                    reporting_manager=user.employee
                )

        for name, field in self.fields.items():

            if name != 'description':

                field.widget.attrs.update(
                    {
                        'class': 'form-control'
                    }
                )
        
    def clean(self):

        cleaned_data = super().clean()

        employee = cleaned_data.get(
            'employee'
        )

        company = cleaned_data.get(
            'company'
        )

        user = getattr(
            self,
            'user',
            None
        )

        if (
            employee
            and user
            and is_manager(user)
        ):

            if (
                employee.reporting_manager
                != user.employee
            ):

                raise forms.ValidationError(
                    'You can only assign tasks to your representatives.'
                )

        if company and employee:

            if (
                company.manager
                != employee.reporting_manager
            ):

                raise forms.ValidationError(
                    'Representative and Company must belong to the same manager.'
                )

        return cleaned_data
            
class CompanyImportForm(forms.Form):
    
    csv_file = forms.FileField()
    
    
    

class AccessRoleForm(forms.ModelForm):

    class Meta:

        model = Role

        fields = [
            "name",
            "description",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    "class": "form-control"
                }
            )

        self.fields["is_active"].widget.attrs["class"] = "form-check-input"