from django import forms
from .models import Company, Employee, Task
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from .utils import * 

class CompanyForm(forms.ModelForm):

    class Meta:

        model = Company

        fields = [
            'name',
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


class EmployeeForm(forms.ModelForm):
    
    username = forms.CharField()

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:

        model = Employee

        fields = [
            'company',
            'role',
            'reporting_manager',
            'designation',
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
    


class EmployeeUpdateForm(forms.ModelForm):

    class Meta:

        model = Employee

        fields = [
            'company',
            'role',
            'reporting_manager',
            'designation',
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

        phone_str = str(phone)

        digits_only = phone_str.replace(
            '+',
            ''
        )

        if not digits_only.isdigit():

            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )

        if len(digits_only) < 10:

            raise forms.ValidationError(
                'Phone number is too short.'
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
            'designation',
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

        phone_str = str(phone)

        digits_only = phone_str.replace(
            '+',
            ''
        )

        if not digits_only.isdigit():

            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )

        if len(digits_only) < 10:

            raise forms.ValidationError(
                'Phone number is too short.'
            )

        return phone_str

    
class TaskForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            'title',
            'description',
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

        if user:

            if is_manager(user):

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
        
    def clean_employee(self):

        employee = self.cleaned_data.get(
            'employee'
        )

        user = getattr(self, 'user', None)

        # ensure employee is present before accessing its attributes
        if employee and user and is_manager(user):
            if employee.reporting_manager != user.employee:
                raise forms.ValidationError(
                    'You can only assign tasks to your representatives.'
                )

        return employee
            
class CompanyImportForm(forms.Form):

    csv_file = forms.FileField()