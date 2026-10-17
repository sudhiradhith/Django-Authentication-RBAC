"""
Generates Lab3B_Report.pdf using ReportLab.
Includes implementation explanations, key code snippets, Expected vs Actual analysis table,
and embedded screenshots.
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)

BASE_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = BASE_DIR / 'screenshots'
OUTPUT_PDF = BASE_DIR / 'Lab3B_Report.pdf'


def generate_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=1, # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0f172a'),
        backColor=colors.HexColor('#f1f5f9'),
        borderColor=colors.HexColor('#cbd5e1'),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1e293b')
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=1,
        spaceBefore=4,
        spaceAfter=10
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("MDSO508-3: Full Stack Web Development", subtitle_style))
    story.append(Paragraph("Lab 3B: Django Authentication &amp; Role-Based Access Control (RBAC)", title_style))
    story.append(Paragraph("<b>Student Submission Report</b> &bull; Built with Django 4.2 LTS &bull; SQLite Database", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceAfter=14))

    # Section 1: Objective & Architecture
    story.append(Paragraph("1. Executive Summary &amp; Architecture", h2_style))
    story.append(Paragraph(
        "This project extends the initial Django application (Lab 3A) by implementing robust user authentication, "
        "a token-based password reset workflow, and Role-Based Access Control (RBAC). "
        "Using Django's built-in <code>User</code> and <code>Group</code> models alongside custom decorators and context processors, "
        "the application strictly segregates permissions across two primary roles: <b>Student</b> and <b>Teacher</b>, "
        "as well as a superuser <b>Admin</b> role.",
        body_style
    ))

    # Architecture Overview Table
    arch_data = [
        [Paragraph("Component", table_header_style), Paragraph("Implementation Mechanism", table_header_style), Paragraph("Key Behaviors &amp; Security Controls", table_header_style)],
        [Paragraph("<b>Signup &amp; Role Assignment</b>", table_cell_style), Paragraph("Custom <code>RegisterForm(UserCreationForm)</code>", table_cell_style), Paragraph("Validates email uniqueness and hashes passwords using PBKDF2_SHA256; automatically assigns user to chosen <code>Group</code>.", table_cell_style)],
        [Paragraph("<b>User Authentication</b>", table_cell_style), Paragraph("<code>authenticate()</code>, <code>login()</code>, <code>logout()</code>", table_cell_style), Paragraph("Session-based state management; preserves <code>?next=</code> parameter for protected route redirects.", table_cell_style)],
        [Paragraph("<b>Protected Page</b>", table_cell_style), Paragraph("<code>@login_required(login_url='login')</code>", table_cell_style), Paragraph("Restricts general dashboard to authenticated users; unauthorized visitors receive HTTP 302 redirect.", table_cell_style)],
        [Paragraph("<b>Password Reset</b>", table_cell_style), Paragraph("Django built-in <code>PasswordResetView</code> suite", table_cell_style), Paragraph("Generates cryptographically secure one-time tokens and logs dispatch via <code>console.EmailBackend</code>.", table_cell_style)],
        [Paragraph("<b>RBAC Enforcement</b>", table_cell_style), Paragraph("Custom <code>@role_required(['Role'])</code> decorator", table_cell_style), Paragraph("Checks user group membership; yields <b>HTTP 403 Access Denied</b> if role is mismatched.", table_cell_style)],
    ]
    arch_table = Table(arch_data, colWidths=[130, 160, 240])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 12))

    # Section 2: Key Code Snippets
    story.append(Paragraph("2. Key Code Implementations", h2_style))
    story.append(Paragraph("<b>A. Role-Based Access Control Decorator (<code>accounts/decorators.py</code>)</b>", body_style))
    snippet_decorator = (
        "def role_required(allowed_roles=None):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;def decorator(view_func):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@wraps(view_func)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;def _wrapped(request, *args, **kwargs):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if not request.user.is_authenticated:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return redirect(f'/login/?next={request.path}')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if request.user.is_superuser:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return view_func(request, *args, **kwargs)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user_groups = list(request.user.groups.values_list('name', flat=True))<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if any(role in user_groups for role in allowed_roles):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return view_func(request, *args, **kwargs)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return render(request, 'accounts/access_denied.html', status=403)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return _wrapped<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return decorator"
    )
    story.append(Paragraph(snippet_decorator, code_style))

    story.append(Paragraph("<b>B. Automatic Group Assignment in Registration Form (<code>accounts/forms.py</code>)</b>", body_style))
    snippet_form = (
        "class RegisterForm(UserCreationForm):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;role = forms.ChoiceField(choices=[('Student','Student'), ('Teacher','Teacher')])<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;def save(self, commit=True):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user = super().save(commit=commit)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;role_name = self.cleaned_data.get('role')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if role_name:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;group, _ = Group.objects.get_or_create(name=role_name)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user.groups.add(group)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return user"
    )
    story.append(Paragraph(snippet_form, code_style))

    story.append(PageBreak())

    # Section 3: Testing & Analysis Matrix
    story.append(Paragraph("3. Testing &amp; Analysis Matrix (Expected vs. Actual Behaviour)", h2_style))
    story.append(Paragraph(
        "The application was thoroughly verified across all user states and roles using both Django automated unit tests "
        "(13 automated test cases) and manual browser inspection. All test outcomes matched expected behaviors.",
        body_style
    ))

    matrix_data = [
        [
            Paragraph("Test Case", table_header_style),
            Paragraph("User Role", table_header_style),
            Paragraph("Target Endpoint", table_header_style),
            Paragraph("Expected Behaviour", table_header_style),
            Paragraph("Actual Behaviour", table_header_style),
            Paragraph("Status", table_header_style)
        ],
        [
            Paragraph("TC-01: Anonymous Access to Protected Dashboard", table_cell_style),
            Paragraph("Unauthenticated", table_cell_style),
            Paragraph("<code>/dashboard/</code>", table_cell_style),
            Paragraph("HTTP 302 Redirect to <code>/login/?next=/dashboard/</code>", table_cell_style),
            Paragraph("Redirected to login with ?next= preserved.", table_cell_style),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_style),
        ],
        [
            Paragraph("TC-02: Valid User Authentication", table_cell_style),
            Paragraph("Any Registered User", table_cell_style),
            Paragraph("<code>/login/</code>", table_cell_style),
            Paragraph("Authenticates session; redirects to dashboard with welcome message.", table_cell_style),
            Paragraph("Session started; redirected to /dashboard/.", table_cell_style),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_style),
        ],
        [
            Paragraph("TC-03: Invalid Login Attempt", table_cell_style),
            Paragraph("Any User", table_cell_style),
            Paragraph("<code>/login/</code>", table_cell_style),
            Paragraph("Rejects submission; displays 'Invalid username or password'.", table_cell_style),
            Paragraph("Form reloaded with error prompt; no session created.", table_cell_style),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_style),
        ],
        [
            Paragraph("TC-04: Student Accessing Student Portal", table_cell_style),
            Paragraph("Student (<code>alice_student</code>)", table_cell_style),
            Paragraph("<code>/student-dashboard/</code>", table_cell_style),
            Paragraph("HTTP 200 OK; displays courses, grades, and deadlines.", table_cell_style),
            Paragraph("Full student interface rendered with course list.", table_cell_style),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_style),
        ],
        [
            Paragraph("TC-05: Student Accessing Teacher Portal", table_cell_style),
            Paragraph("Student (<code>alice_student</code>)", table_cell_style),
            Paragraph("<code>/teacher-dashboard/</code>", table_cell_style),
            Paragraph("<b>HTTP 403 Forbidden</b>; renders friendly Access Denied page.", table_cell_style),
            Paragraph("HTTP 403 returned; displays Access Denied page indicating role conflict.", table_cell_style),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_style),
        ],
        [
            Paragraph("TC-06: Teacher Accessing Teacher Portal", table_cell_style),
            Paragraph("Teacher (<code>prof_smith</code>)", table_cell_style),
            Paragraph("<code>/teacher-dashboard/</code>", table_cell_style),
            Paragraph("HTTP 200 OK; displays student roster and assignment review table.", table_cell_style),
            Paragraph("Instructor management interface displayed successfully.", table_cell_style),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_style),
        ],
        [
            Paragraph("TC-07: Admin Access to All Dashboards", table_cell_style),
            Paragraph("Superuser (<code>admin</code>)", table_cell_style),
            Paragraph("Student &amp; Teacher Dashboards", table_cell_style),
            Paragraph("HTTP 200 OK; superuser bypass grants full access to both.", table_cell_style),
            Paragraph("Access granted to all endpoints without restriction.", table_cell_style),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_style),
        ],
        [
            Paragraph("TC-08: Token-Based Password Reset", table_cell_style),
            Paragraph("Registered User", table_cell_style),
            Paragraph("<code>/password-reset/</code>", table_cell_style),
            Paragraph("Dispatches one-time token link to console email backend.", table_cell_style),
            Paragraph("Token link generated and printed to console; confirm view updates password.", table_cell_style),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_style),
        ],
        [
            Paragraph("TC-09: User Logout", table_cell_style),
            Paragraph("Authenticated User", table_cell_style),
            Paragraph("<code>/logout/</code>", table_cell_style),
            Paragraph("Session flushed; redirects to login with confirmation message.", table_cell_style),
            Paragraph("User logged out; session destroyed; login page displayed.", table_cell_style),
            Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_style),
        ],
    ]

    matrix_table = Table(matrix_data, colWidths=[100, 75, 85, 130, 105, 35])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(matrix_table)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Section 4: Visual Screenshots Gallery
    story.append(Paragraph("4. Visual Verification &amp; Screenshots Gallery", h2_style))
    story.append(Paragraph(
        "Below are high-resolution captures of the live application demonstrating the key workflows: "
        "User Signup &amp; Role Selection, Authentication, Protected Dashboard, Student &amp; Teacher Portals, "
        "and RBAC Access Denied enforcement.",
        body_style
    ))

    screenshots_to_include = [
        ("01_home_page.png", "Figure 1: Home Page with Project Overview, Feature List, and Pre-Configured Test Accounts"),
        ("02_registration_page.png", "Figure 2: User Registration Form with Role Selection Dropdown (Student / Teacher)"),
        ("03_login_page.png", "Figure 3: User Login Form with Session Authentication and Password Recovery Link"),
        ("04_protected_dashboard.png", "Figure 4: General Protected Dashboard (Protected via @login_required)"),
        ("05_student_portal.png", "Figure 5: Student Portal with Enrolled Courses, Grades, and Deadlines (Role: Student)"),
        ("06_teacher_portal.png", "Figure 6: Teacher Portal with Student Roster and Assignment Review Table (Role: Teacher)"),
        ("07_access_denied_403.png", "Figure 7: HTTP 403 Access Denied when Student attempts to visit Teacher Portal"),
        ("08_password_reset_request.png", "Figure 8: Password Reset Request Form generating token-based recovery link"),
        ("09_password_reset_sent.png", "Figure 9: Password Reset Email Confirmation with Developer Console Output Note"),
    ]

    for filename, caption in screenshots_to_include:
        img_path = SCREENSHOTS_DIR / filename
        if img_path.exists():
            element_block = []
            # Width: 480px, Height: 240px preserves clean layout
            element_block.append(Image(str(img_path), width=480, height=240))
            element_block.append(Paragraph(caption, caption_style))
            element_block.append(Spacer(1, 10))
            story.append(KeepTogether(element_block))

    doc.build(story)
    print(f"Report successfully compiled: {OUTPUT_PDF}")


if __name__ == '__main__':
    generate_pdf()
