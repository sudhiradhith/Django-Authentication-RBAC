"""
Context processors for accounts app.

Provides user role information to all templates automatically.
"""

def user_role_context(request):
    """
    Exposes the active user's primary role and group memberships to all templates.
    """
    if request.user.is_authenticated:
        groups = list(request.user.groups.values_list('name', flat=True))
        if request.user.is_superuser:
            primary_role = "Admin"
        elif groups:
            primary_role = groups[0]
        else:
            primary_role = "General User"
        return {
            'user_role': primary_role,
            'user_roles': groups,
            'is_student': 'Student' in groups or request.user.is_superuser,
            'is_teacher': 'Teacher' in groups or request.user.is_superuser,
        }
    return {
        'user_role': None,
        'user_roles': [],
        'is_student': False,
        'is_teacher': False,
    }
