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
    
    
def is_representative(user):

    return user.groups.filter(
        name='Representative'
    ).exists()


def manager_or_admin(user):

    return (
        is_admin(user)
        or
        is_manager(user)
    )