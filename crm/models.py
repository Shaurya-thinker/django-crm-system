from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Company(models.Model):

    name = models.CharField(
        max_length=200
    )
    
    manager = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='companies',
        limit_choices_to={
            'role': 'manager'
        }
    )

    slug = models.SlugField(
        blank=True
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    
    class Meta:
        verbose_name_plural = 'Companies'


    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(
                self.name
            )

        super().save(
            *args,
            **kwargs
        )

    def __str__(self):

        return self.name


class Employee(models.Model):

    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('representative', 'Representative'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    
    access_role = models.ForeignKey(
        'Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees"
    )

    reporting_manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='representatives'
    )

    phone = models.CharField(
        max_length=20
    )

    profile_image = models.ImageField(
        upload_to='employee_profiles/',
        blank=True,
        null=True
    )

    def __str__(self):

        return self.user.username
    


class Role(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return self.name
    
    

class Permission(models.Model):

    code = models.CharField(
        max_length=100,
        unique=True
    )

    name = models.CharField(
        max_length=150
    )

    module = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):

        return self.name
    
    

class RolePermission(models.Model):

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE
    )

    class Meta:

        unique_together = (
            'role',
            'permission'
        )

    def __str__(self):

        return f"{self.role} - {self.permission}"



class Task(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    deadline = models.DateTimeField()

    attachment = models.FileField(
        upload_to='task_attachments/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title