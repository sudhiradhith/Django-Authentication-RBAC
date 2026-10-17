# Full Stack Web Development (MDSO508-3)
## Lab 3B: Django User Authentication & Role-Based Access Control (RBAC)

A complete, beginner-friendly Django application demonstrating session-based user authentication, token-based password reset, and Role-Based Access Control (RBAC) using Django's built-in framework.

---

## 📌 Project Overview & Objectives

This project satisfies all requirements for **Lab 3B**:
- **Task 1: User Authentication**
  - **Signup/Registration:** Users register with Username, Email, Password, Confirmation, and Role selection.
  - **Login:** Session-based authentication with `?next=` redirection and invalid credential handling.
  - **Logout:** Session termination with flash confirmation.
  - **Protected Page:** General Dashboard (`/dashboard/`) strictly restricted via `@login_required`.
- **Task 2: Password Reset Workflow**
  - Implemented using Django's built-in `PasswordResetView`, `PasswordResetDoneView`, `PasswordResetConfirmView`, and `PasswordResetCompleteView`.
  - Dispatches secure token links using Django's `console.EmailBackend` (output printed to the terminal).
- **Task 3: Role-Based Access Control (RBAC)**
  - Two distinct user roles implemented with Django's built-in `Group` model: **Student** and **Teacher** (plus superuser **Admin**).
  - Custom `@role_required(['Role'])` decorator restricts access to role-specific views.
  - **Student Portal (`/student-dashboard/`):** Accessible to Students (courses, submissions, grades).
  - **Teacher Portal (`/teacher-dashboard/`):** Accessible strictly to Teachers (student roster, grading controls).
  - **Access Denied Page (`/access-denied/`):** Returns **HTTP 403 Forbidden** with clear explanation of role conflict when unauthorized users attempt access.
- **Task 4: Testing & Analysis**
  - Comprehensive automated unit test suite (13 tests in `accounts/tests.py`).
  - Expected vs. Actual Behaviour Analysis table.
  - Real screenshots captured via headless browser in `screenshots/`.
  - Professional PDF Report generated via ReportLab (`Lab3B_Report.pdf`).
  - Source code zipped for submission (`Lab3B_Project.zip`).

---

## 🗂️ Project Directory Structure

```text
lab3b/
├── db.sqlite3                # Pre-seeded SQLite database with roles & test users
├── django_version.txt        # Verified Django version (4.2.7)
├── requirements.txt          # Python dependencies
├── README.md                 # Complete documentation & test guide
├── manage.py                 # Django administrative tool
│
├── myproject/                # Project Settings & Root Routing
│   ├── settings.py           # Auth redirect URLs, console email, RBAC context processor
│   ├── urls.py               # Main URL dispatcher
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                 # Accounts & RBAC Application
│   ├── admin.py              # Admin configuration
│   ├── apps.py               # App configuration
│   ├── context_processors.py # Exposes active user role to all templates
│   ├── decorators.py         # @role_required decorator with 403 handling
│   ├── forms.py              # RegisterForm with Role dropdown & UserLoginForm
│   ├── models.py             # Uses Django's built-in User & Group models
│   ├── tests.py              # 13 automated unit tests
│   ├── urls.py               # Authentication, RBAC dashboards & password reset routes
│   ├── views.py              # View controllers
│   ├── management/commands/
│   │   └── setup_roles.py    # Management command: python manage.py setup_roles
│   └── templates/accounts/
│       ├── base.html         # Responsive base layout with role pill & nav
│       ├── home.html         # Portal overview & test account matrix
│       ├── login.html        # Login form with ?next= handler
│       ├── register.html     # Signup form with Role selection
│       ├── dashboard.html    # Protected general dashboard (@login_required)
│       ├── student_dashboard.html # Student-only protected view
│       ├── teacher_dashboard.html # Teacher-only protected view
│       ├── access_denied.html     # 403 Access Denied explanation page
│       ├── password_reset.html    # Step 1: Request reset
│       ├── password_reset_done.html # Step 2: Email dispatched notice
│       ├── password_reset_confirm.html # Step 3: Enter new password
│       └── password_reset_complete.html# Step 4: Reset success page
│
├── screenshots/              # Real rendered screenshots (PNG)
├── setup_roles.py            # Standalone database seed script
├── render_and_capture.py     # Headless browser screenshot generator
├── generate_pdf_report.py    # ReportLab script producing Lab3B_Report.pdf
├── package_project.py        # Compiles Lab3B_Project.zip
├── Lab3B_Report.pdf          # Short PDF report for submission
└── Lab3B_Project.zip         # Packaged project archive for submission
```

---

## 🚀 Quick Start Guide

### Step 1: Open Terminal in `lab3b` Directory
```powershell
cd "c:\Users\User\Downloads\Lab3A_Django (1)\lab3b"
```

### Step 2: Apply Database Migrations & Seed Roles / Users
```powershell
python setup_roles.py
```
*(Or run `python manage.py setup_roles`)*

### Step 3: Run the Development Server
```powershell
python manage.py runserver
```

Open your browser to:
- **Home Page:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Login:** [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
- **Register:** [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)
- **Protected Dashboard:** [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- **Student Portal:** [http://127.0.0.1:8000/student-dashboard/](http://127.0.0.1:8000/student-dashboard/)
- **Teacher Portal:** [http://127.0.0.1:8000/teacher-dashboard/](http://127.0.0.1:8000/teacher-dashboard/)
- **Password Reset:** [http://127.0.0.1:8000/password-reset/](http://127.0.0.1:8000/password-reset/)
- **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Pre-Configured Test Accounts

The SQLite database is pre-seeded with these test credentials:

| Role | Username | Email | Password | Allowed Access |
|---|---|---|---|---|
| **Student** | `alice_student` | `alice@example.com` | `Student@123` | Dashboard, Student Portal |
| **Teacher** | `prof_smith` | `prof_smith@example.com` | `Teacher@123` | Dashboard, Teacher Portal |
| **Admin (Superuser)** | `admin` | `admin@example.com` | `Admin@123` | Full Access + Django Admin |

---

## 🧪 Testing Guide

### 1. Test User Authentication (Task 1)
- **Unauthenticated Check:** While logged out, visit [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/). Notice you are automatically redirected to `/login/?next=/dashboard/`.
- **Login:** Log in with `alice_student` / `Student@123`. You are redirected directly to your protected dashboard with the "Student" role badge.
- **Logout:** Click **Logout**. The session is terminated and you are returned to login with a confirmation message.

### 2. Test Password Reset Workflow (Task 2)
1. Go to [http://127.0.0.1:8000/password-reset/](http://127.0.0.1:8000/password-reset/).
2. Enter `alice@example.com` and submit.
3. Check your running server terminal &mdash; Django's console email backend prints the reset email containing the token link:
   `http://127.0.0.1:8000/reset/<uidb64>/<token>/`
4. Copy and open that link in your browser.
5. Enter a new password and confirm.
6. Log in with the new password to confirm successful reset!

### 3. Test Role-Based Access Control (RBAC) (Task 3)
- **Test Student Access:**
  - Log in as `alice_student`.
  - Visit [http://127.0.0.1:8000/student-dashboard/](http://127.0.0.1:8000/student-dashboard/) &rarr; **Access Granted (HTTP 200)**.
  - Attempt to visit [http://127.0.0.1:8000/teacher-dashboard/](http://127.0.0.1:8000/teacher-dashboard/) &rarr; **Access Denied (HTTP 403)** with error prompt stating your role (`Student`) does not match the required role (`Teacher`).
- **Test Teacher Access:**
  - Log in as `prof_smith`.
  - Visit [http://127.0.0.1:8000/teacher-dashboard/](http://127.0.0.1:8000/teacher-dashboard/) &rarr; **Access Granted (HTTP 200)**. Student roster and grading controls are accessible.
- **Test Admin Bypass:**
  - Log in as `admin`. Both Student and Teacher dashboards are fully accessible.

---

## 🧪 Automated Unit Tests

Run the full test suite in `lab3b`:
```powershell
python manage.py test
```

Expected result:
```text
Found 13 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.............
----------------------------------------------------------------------
Ran 13 tests in 21s

OK
Destroying test database for alias 'default'...
```

---

## 📄 Submission Files

The project includes all required submission items ready to submit:
1. **Source Code Zip Archive:** `Lab3B_Project.zip`
2. **Short PDF Report:** `Lab3B_Report.pdf` (contains implementation explanations, code snippets, Expected vs. Actual behavior table, and high-resolution screenshots).
