from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Sets up initial roles and demo accounts for Lab 3B.'

    def handle(self, *args, **options):
        student_group, _ = Group.objects.get_or_create(name='Student')
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        self.stdout.write(self.style.SUCCESS("Ensured groups: Student, Teacher"))

        # Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'Admin@123')
            self.stdout.write(self.style.SUCCESS("Created Superuser: admin (Admin@123)"))

        # Student
        if not User.objects.filter(username='alice_student').exists():
            u = User.objects.create_user('alice_student', 'alice@example.com', 'Student@123')
            u.groups.add(student_group)
            self.stdout.write(self.style.SUCCESS("Created Student: alice_student (Student@123)"))

        # Teacher
        if not User.objects.filter(username='prof_smith').exists():
            t = User.objects.create_user('prof_smith', 'prof_smith@example.com', 'Teacher@123')
            t.groups.add(teacher_group)
            self.stdout.write(self.style.SUCCESS("Created Teacher: prof_smith (Teacher@123)"))

        self.stdout.write(self.style.SUCCESS("Role setup completed successfully."))
