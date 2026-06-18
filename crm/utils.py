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


def manager_or_admin(user):

    return (
        is_admin(user)
        or
        is_manager(user)
    )