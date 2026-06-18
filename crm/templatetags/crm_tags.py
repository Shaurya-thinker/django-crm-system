from django import template

register = template.Library()


@register.filter
def has_group(user, group_name):

    return user.groups.filter(
        name=group_name
    ).exists()
    
@register.filter
def is_representative(user):

    if hasattr(user, 'employee'):

        return (
            user.employee.role
            ==
            'representative'
        )

    return False

@register.filter
def is_manager(user):

    if hasattr(user, 'employee'):

        return (
            user.employee.role
            ==
            'manager'
        )

    return False