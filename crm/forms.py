from django import forms
from .models import Company, Employee, Task
from ckeditor.widgets import CKEditorWidget

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

    class Meta:

        model = Employee

        fields = [
            'user',
            'company',
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

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if name != 'description':

                field.widget.attrs.update(
                    {
                        'class': 'form-control'
                    }
                )
            
class CompanyImportForm(forms.Form):

    csv_file = forms.FileField()