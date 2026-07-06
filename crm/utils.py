def is_admin(user):

    return user.groups.filter(
        name='Admin'
    ).exists()


def is_manager(user):

    return (
        hasattr(user, 'employee')
        and user.employee.role == 'manager'
    )
    
    
def is_representative(user):

    return (
        hasattr(user, 'employee')
        and user.employee.role == 'representative'
    )
    
    
    
from .models import RolePermission


def has_permission(user, permission_code):

    if is_admin(user):
        return True

    if not hasattr(user, "employee"):
        return False

    role = user.employee.access_role

    if role is None:
        return False

    return RolePermission.objects.filter(
        role=role,
        permission__code=permission_code
    ).exists()


from django.conf import settings

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from django.utils.html import strip_tags


def send_notification_email(
    subject,
    template_name,
    context,
    recipient_list,
):

    html_content = render_to_string(
        template_name,
        context
    )

    text_content = strip_tags(
        html_content
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )

    email.attach_alternative(
        html_content,
        "text/html"
    )

    email.send()