"""
Role and Test Data Setup Script for Lab 3B.

Creates:
1. Groups: 'Student', 'Teacher'
2. Superuser: 'admin' (password: Admin@123)
3. Student User: 'alice_student' (password: Student@123)
4. Teacher User: 'prof_smith' (password: Teacher@123)
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User, Group


def setup():
    print("Applying database migrations...")
    call_command('migrate', verbosity=1)

    print("\nSetting up Roles / Groups...")
    student_group, _ = Group.objects.get_or_create(name='Student')
    teacher_group, _ = Group.objects.get_or_create(name='Teacher')
    print("Groups ensured: Student, Teacher")

    print("\nCreating demo accounts...")

    # 1. Admin / Superuser
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'Admin@123')
        print("Created Superuser: admin (Admin@123)")
    else:
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('Admin@123')
        admin_user.save()
        print("Updated Superuser: admin")

    # 2. Student User: alice_student
    if not User.objects.filter(username='alice_student').exists():
        student_user = User.objects.create_user('alice_student', 'alice@example.com', 'Student@123')
        student_user.groups.add(student_group)
        print("Created Student: alice_student (Student@123)")
    else:
        student_user = User.objects.get(username='alice_student')
        student_user.groups.add(student_group)
        student_user.set_password('Student@123')
        student_user.save()
        print("Updated Student: alice_student")

    # 3. Teacher User: prof_smith
    if not User.objects.filter(username='prof_smith').exists():
        teacher_user = User.objects.create_user('prof_smith', 'prof_smith@example.com', 'Teacher@123')
        teacher_user.groups.add(teacher_group)
        print("Created Teacher: prof_smith (Teacher@123)")
    else:
        teacher_user = User.objects.get(username='prof_smith')
        teacher_user.groups.add(teacher_group)
        teacher_user.set_password('Teacher@123')
        teacher_user.save()
        print("Updated Teacher: prof_smith")

    print("\n--- Summary of Registered Users in Database ---")
    for u in User.objects.all():
        roles = list(u.groups.values_list('name', flat=True))
        status = "Superuser" if u.is_superuser else (roles[0] if roles else "No Role")
        print(f"Username: {u.username:<15} Email: {u.email:<22} Role: {status}")


if __name__ == '__main__':
    setup()
