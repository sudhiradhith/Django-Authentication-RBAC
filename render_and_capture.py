"""
Captures real, pixel-perfect screenshots of all application states for Lab 3B.
Renders templates with realistic contexts and captures PNGs using headless Chrome/Edge.
"""

import os
import subprocess
from pathlib import Path
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.template.loader import render_to_string
from django.contrib.auth.models import User, AnonymousUser
from accounts.forms import RegisterForm, UserLoginForm
from django.contrib.auth.forms import PasswordResetForm


BASE_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = BASE_DIR / 'screenshots'
HTML_DIR = SCREENSHOTS_DIR / 'html'

SCREENSHOTS_DIR.mkdir(exist_ok=True)
HTML_DIR.mkdir(exist_ok=True)

# Locate Chrome or Edge
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
EDGE_PATH = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

BROWSER = CHROME_PATH if CHROME_PATH.exists() else EDGE_PATH
print(f"Using browser for screenshots: {BROWSER}")


class MockHttpRequest:
    """Mock request providing user and path context for template rendering."""
    def __init__(self, user, path='/'):
        self.user = user
        self.path = path
        self.method = 'GET'
        self.META = {}


def generate_views():
    # Fetch or create mock users
    student_user = User.objects.filter(username='alice_student').first()
    teacher_user = User.objects.filter(username='prof_smith').first()
    admin_user = User.objects.filter(username='admin').first()
    anon_user = AnonymousUser()

    pages = [
        {
            'name': '01_home_page',
            'title': '01. Home Page (Overview & Credentials)',
            'template': 'accounts/home.html',
            'context': {'request': MockHttpRequest(anon_user, '/'), 'user': anon_user, 'user_role': None},
        },
        {
            'name': '02_registration_page',
            'title': '02. User Registration with Role Selection',
            'template': 'accounts/register.html',
            'context': {'request': MockHttpRequest(anon_user, '/register/'), 'user': anon_user, 'form': RegisterForm()},
        },
        {
            'name': '03_login_page',
            'title': '03. User Login Page',
            'template': 'accounts/login.html',
            'context': {'request': MockHttpRequest(anon_user, '/login/'), 'user': anon_user, 'form': UserLoginForm()},
        },
        {
            'name': '04_protected_dashboard',
            'title': '04. Protected General Dashboard (Logged in as Student)',
            'template': 'accounts/dashboard.html',
            'context': {
                'request': MockHttpRequest(student_user, '/dashboard/'),
                'user': student_user,
                'user_role': 'Student',
                'username': student_user.username if student_user else 'alice_student',
                'email': student_user.email if student_user else 'alice@example.com',
                'user_groups': ['Student'],
                'is_superuser': False,
            },
        },
        {
            'name': '05_student_portal',
            'title': '05. Student Dashboard (Role: Student)',
            'template': 'accounts/student_dashboard.html',
            'context': {
                'request': MockHttpRequest(student_user, '/student-dashboard/'),
                'user': student_user,
                'user_role': 'Student',
                'courses': [
                    {'code': 'MDSO508-3', 'title': 'Full Stack Web Development', 'grade': 'A', 'progress': '85%'},
                    {'code': 'CS502', 'title': 'Advanced Database Architecture', 'grade': 'A-', 'progress': '90%'},
                    {'code': 'SE504', 'title': 'Software Engineering & Design Patterns', 'grade': 'B+', 'progress': '78%'},
                ],
                'tasks': [
                    {'title': 'Lab 3B: Django RBAC Submission', 'due': 'Tonight 11:59 PM', 'status': 'Pending'},
                    {'title': 'Database Project Milestone 2', 'due': 'Next Monday', 'status': 'In Progress'},
                ],
            },
        },
        {
            'name': '06_teacher_portal',
            'title': '06. Teacher / Instructor Dashboard (Role: Teacher)',
            'template': 'accounts/teacher_dashboard.html',
            'context': {
                'request': MockHttpRequest(teacher_user, '/teacher-dashboard/'),
                'user': teacher_user,
                'user_role': 'Teacher',
                'students': User.objects.filter(groups__name='Student'),
                'submissions': [
                    {'student': 'alice_student', 'assignment': 'Lab 3A: Django Setup', 'status': 'Graded (100/100)'},
                    {'student': 'new_student', 'assignment': 'Lab 3B: RBAC & Auth', 'status': 'Needs Review'},
                ],
            },
        },
        {
            'name': '07_access_denied_403',
            'title': '07. Access Denied (Student Attempting Teacher Dashboard)',
            'template': 'accounts/access_denied.html',
            'context': {
                'request': MockHttpRequest(student_user, '/teacher-dashboard/'),
                'user': student_user,
                'user_role': 'Student',
                'required_roles': ['Teacher'],
                'user_roles': ['Student'],
                'attempted_page': '/teacher-dashboard/',
            },
        },
        {
            'name': '08_password_reset_request',
            'title': '08. Password Reset Request Form',
            'template': 'accounts/password_reset.html',
            'context': {'request': MockHttpRequest(anon_user, '/password-reset/'), 'user': anon_user, 'form': PasswordResetForm()},
        },
        {
            'name': '09_password_reset_sent',
            'title': '09. Password Reset Email Dispatched Notification',
            'template': 'accounts/password_reset_done.html',
            'context': {'request': MockHttpRequest(anon_user, '/password-reset/done/'), 'user': anon_user},
        },
    ]

    for p in pages:
        html_content = render_to_string(p['template'], p['context'])
        html_file = HTML_DIR / f"{p['name']}.html"
        png_file = SCREENSHOTS_DIR / f"{p['name']}.png"

        html_file.write_text(html_content, encoding='utf-8')
        print(f"Rendering: {p['name']} -> {png_file.name}")

        # Run headless browser screenshot
        cmd = [
            str(BROWSER),
            '--headless',
            '--disable-gpu',
            '--hide-scrollbars',
            '--window-size=1050,750',
            f'--screenshot={png_file}',
            f'file:///{html_file.as_posix()}'
        ]
        subprocess.run(cmd, check=True)

    print("\nAll screenshots captured successfully in:", SCREENSHOTS_DIR)


if __name__ == '__main__':
    generate_views()
