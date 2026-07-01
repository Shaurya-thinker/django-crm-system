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