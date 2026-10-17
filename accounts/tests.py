"""
Automated unit tests for Lab 3B: Authentication & Role-Based Access Control (RBAC).

Tests:
1. Task 1: Registration, Login, Logout, Protected Dashboard.
2. Task 2: Password Reset Workflow (Request, Token generation, Confirm, Complete).
3. Task 3: RBAC (Group assignment, Decorator behavior, 403 Access Denied, Superuser bypass).
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core import mail
from accounts.forms import RegisterForm


class UserAuthenticationTests(TestCase):
    """Task 1: Tests for User Registration, Login, Logout, and Protected Dashboard."""

    def setUp(self):
        self.client = Client()
        self.student_group, _ = Group.objects.get_or_create(name='Student')
        self.teacher_group, _ = Group.objects.get_or_create(name='Teacher')

    def test_signup_creates_user_with_role(self):
        """Registering with 'Student' role creates user and attaches them to Student group."""
        data = {
            'username': 'new_student',
            'email': 'student@university.edu',
            'role': 'Student',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        response = self.client.post(reverse('register'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Verify user in database
        user = User.objects.get(username='new_student')
        self.assertEqual(user.email, 'student@university.edu')
        self.assertTrue(user.groups.filter(name='Student').exists())

    def test_login_success_and_redirect(self):
        """Logging in with valid credentials creates session and redirects to dashboard."""
        User.objects.create_user('valid_user', 'user@example.com', 'ValidPass123!')
        login_data = {'username': 'valid_user', 'password': 'ValidPass123!'}
        response = self.client.post(reverse('login'), data=login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_failure_invalid_credentials(self):
        """Invalid credentials show error and reject login."""
        User.objects.create_user('valid_user', 'user@example.com', 'ValidPass123!')
        login_data = {'username': 'valid_user', 'password': 'WrongPassword!'}
        response = self.client.post(reverse('login'), data=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_logout(self):
        """Logging out terminates session and redirects to login."""
        user = User.objects.create_user('logout_user', 'out@example.com', 'Pass123!')
        self.client.force_login(user)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_protected_dashboard_redirects_anonymous_user(self):
        """Unauthenticated visitor to /dashboard/ is redirected to /login/?next=/dashboard/."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_protected_dashboard_accessible_to_authenticated_user(self):
        """Authenticated user can access /dashboard/ successfully."""
        user = User.objects.create_user('auth_user', 'auth@example.com', 'Pass123!')
        self.client.force_login(user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User Dashboard (Protected Page)")


class PasswordResetTests(TestCase):
    """Task 2: Tests for Django Built-in Password Reset Workflow."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('reset_user', 'reset@university.edu', 'InitialPass123!')

    def test_password_reset_page_loads(self):
        """Password reset request form loads with 200 OK."""
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reset Your Password")

    def test_password_reset_email_dispatched(self):
        """Submitting email generates a reset token and sends email via console backend."""
        response = self.client.post(reverse('password_reset'), {'email': 'reset@university.edu'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password Reset Sent")

        # Verify an email was sent in test outbox
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('reset_user', mail.outbox[0].body)
        self.assertIn('/reset/', mail.outbox[0].body)


class RoleBasedAccessControlTests(TestCase):
    """Task 3: Tests for Role-Based Access Control (RBAC)."""

    def setUp(self):
        self.client = Client()
        self.student_group, _ = Group.objects.get_or_create(name='Student')
        self.teacher_group, _ = Group.objects.get_or_create(name='Teacher')

        # Create Student
        self.student = User.objects.create_user('alice_student', 'alice@test.com', 'Student@123')
        self.student.groups.add(self.student_group)

        # Create Teacher
        self.teacher = User.objects.create_user('prof_smith', 'prof@test.com', 'Teacher@123')
        self.teacher.groups.add(self.teacher_group)

        # Create Admin
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'Admin@123')

    def test_student_can_access_student_dashboard(self):
        """User in Student group can view /student-dashboard/."""
        self.client.force_login(self.student)
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Portal")

    def test_student_cannot_access_teacher_dashboard(self):
        """User in Student group is DENIED (HTTP 403) when attempting /teacher-dashboard/."""
        self.client.force_login(self.student)
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "403 - Access Denied", status_code=403)
        self.assertContains(response, "Teacher", status_code=403)

    def test_teacher_can_access_teacher_dashboard(self):
        """User in Teacher group can view /teacher-dashboard/."""
        self.client.force_login(self.teacher)
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teacher / Instructor Portal")

    def test_admin_has_full_access(self):
        """Superuser/Admin can access both student and teacher dashboards."""
        self.client.force_login(self.admin)
        res_student = self.client.get(reverse('student_dashboard'))
        res_teacher = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(res_student.status_code, 200)
        self.assertEqual(res_teacher.status_code, 200)

    def test_anonymous_user_redirected_to_login(self):
        """Anonymous visitor to any restricted dashboard is redirected to login."""
        res1 = self.client.get(reverse('student_dashboard'))
        res2 = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(res1.status_code, 302)
        self.assertEqual(res2.status_code, 302)
        self.assertIn(reverse('login'), res1.url)
        self.assertIn(reverse('login'), res2.url)
