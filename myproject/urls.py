"""
myproject URL Configuration for Lab 3B.

Routes:
- /admin/ -> Built-in Django Admin Interface
- /       -> accounts.urls (Authentication, RBAC Dashboards, Password Reset)
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
]
