"""
Views for accounts app implementing Authentication & Role-Based Access Control.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, UserLoginForm
from .decorators import role_required


def home(request):
    """
    Public Home Page:
    Displays project overview, requirements, test accounts, and quick access links.
    """
    return render(request, 'accounts/home.html')


def register(request):
    """
    Task 1: User Registration
    Creates a new user account with chosen role (Student or Teacher)
    and saves to database.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            messages.success(
                request,
                f"Account created successfully for '{user.username}' with role '{role}'! Please log in."
            )
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """
    Task 1: User Login
    Authenticates user credentials and redirects to dashboard or 'next' URL.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    next_url = request.GET.get('next', 'dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url if next_url else 'dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm(request)

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def user_logout(request):
    """
    Task 1: User Logout
    Terminates the session and redirects to login with confirmation message.
    Supports both GET and POST requests cleanly.
    """
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f"You have been successfully logged out, {username}.")
    return redirect('login')


@login_required
def dashboard(request):
    """
    Task 1: General Protected Dashboard
    Accessible ONLY to authenticated users. Unauthenticated visitors are redirected.
    """
    user_groups = list(request.user.groups.values_list('name', flat=True))
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'user_groups': user_groups,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'accounts/dashboard.html', context)


@role_required(allowed_roles=['Student'])
def student_dashboard(request):
    """
    Task 3: Student-Only Protected View
    Accessible to users in the 'Student' group (and superusers).
    Students can view course materials, submissions, and grades.
    """
    # Sample academic mock data for the student view
    enrolled_courses = [
        {'code': 'MDSO508-3', 'title': 'Full Stack Web Development', 'grade': 'A', 'progress': '85%'},
        {'code': 'CS502', 'title': 'Advanced Database Architecture', 'grade': 'A-', 'progress': '90%'},
        {'code': 'SE504', 'title': 'Software Engineering & Design Patterns', 'grade': 'B+', 'progress': '78%'},
    ]
    upcoming_tasks = [
        {'title': 'Lab 3B: Django RBAC Submission', 'due': 'Tonight 11:59 PM', 'status': 'Pending'},
        {'title': 'Database Project Milestone 2', 'due': 'Next Monday', 'status': 'In Progress'},
    ]
    return render(request, 'accounts/student_dashboard.html', {
        'courses': enrolled_courses,
        'tasks': upcoming_tasks,
    })


@role_required(allowed_roles=['Teacher'])
def teacher_dashboard(request):
    """
    Task 3: Teacher-Only Protected View
    Accessible ONLY to users in the 'Teacher' group (and superusers).
    Teachers can manage assignments, grade submissions, and view students.
    """
    # Sample mock data for the instructor portal
    all_students = User.objects.filter(groups__name='Student')
    recent_submissions = [
        {'student': 'alice_student', 'assignment': 'Lab 3A: Django Setup', 'status': 'Graded (100/100)'},
        {'student': 'student1', 'assignment': 'Lab 3B: RBAC & Auth', 'status': 'Needs Review'},
        {'student': 'student2', 'assignment': 'Lab 3B: RBAC & Auth', 'status': 'Submitted'},
    ]
    return render(request, 'accounts/teacher_dashboard.html', {
        'students': all_students,
        'submissions': recent_submissions,
    })


def access_denied(request):
    """
    Task 3: Standalone 403 Access Denied explanation page.
    """
    return render(request, 'accounts/access_denied.html', status=403)
