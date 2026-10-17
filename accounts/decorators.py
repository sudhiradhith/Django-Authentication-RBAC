"""
Role-Based Access Control (RBAC) Decorators.

Implements view-level access restriction based on user groups/roles.
"""

from functools import wraps
from django.shortcuts import render, redirect


def role_required(allowed_roles=None):
    """
    Decorator that restricts view access to users belonging to specific groups/roles.
    
    Behavior:
    1. If the user is anonymous, redirects to the login page (with ?next=).
    2. If the user is a superuser, access is automatically granted.
    3. If the user belongs to at least one of the allowed roles, access is granted.
    4. Otherwise, renders the friendly 'access_denied.html' template with HTTP 403.
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Step 1: Authentication check
            if not request.user.is_authenticated:
                return redirect(f"/login/?next={request.path}")

            # Step 2: Superuser bypass
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Step 3: Check group membership
            user_groups = list(request.user.groups.values_list('name', flat=True))
            has_role = any(role in user_groups for role in allowed_roles)

            if has_role:
                return view_func(request, *args, **kwargs)

            # Step 4: Access Denied (HTTP 403)
            context = {
                'required_roles': allowed_roles,
                'user_roles': user_groups if user_groups else ['No Role Assigned'],
                'attempted_page': request.path,
            }
            return render(request, 'accounts/access_denied.html', context, status=403)

        return _wrapped_view
    return decorator
