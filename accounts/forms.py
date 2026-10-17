"""
Forms for user authentication and registration with RBAC.
"""

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


ROLE_CHOICES = (
    ('Student', 'Student (Access course materials, submissions, grades)'),
    ('Teacher', 'Teacher / Instructor (Manage grades, courses, students)'),
)


class RegisterForm(UserCreationForm):
    """
    User registration form with:
    - Username
    - Email (required, unique)
    - Role / Group selection ('Student' or 'Teacher')
    - Password & Password confirmation (handled by UserCreationForm)
    """
    email = forms.EmailField(
        required=True,
        label="Email Address",
        help_text="Required. A valid email address for account and password recovery.",
        widget=forms.EmailInput(attrs={'placeholder': 'name@example.com'})
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        initial='Student',
        required=True,
        label="Account Role",
        help_text="Select your role to configure role-based access permissions.",
        widget=forms.Select(attrs={'class': 'role-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        """Enforces case-insensitive email uniqueness."""
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def save(self, commit=True):
        """Saves user and automatically binds them to the chosen Role/Group."""
        user = super().save(commit=commit)
        role_name = self.cleaned_data.get('role')
        if role_name:
            group, _ = Group.objects.get_or_create(name=role_name)
            user.groups.add(group)
        return user


class UserLoginForm(AuthenticationForm):
    """
    Custom styled login form based on Django's built-in AuthenticationForm.
    """
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter username', 'autofocus': True})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )
