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

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employees'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    reporting_manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='representatives'
    )

    designation = models.CharField(
        max_length=100
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