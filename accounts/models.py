"""
Models for accounts application.

In this project, we utilize Django's built-in User and Group models:
- django.contrib.auth.models.User: Manages user accounts, credentials, and profile info.
- django.contrib.auth.models.Group: Represents user roles ('Student', 'Teacher', etc.)
  for Role-Based Access Control (RBAC).
"""

from django.db import models

# No custom models required; Django's built-in User & Group models satisfy all RBAC requirements.
