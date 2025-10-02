from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import OfferedCourse

class Command(BaseCommand):
    help = "Create Students, Institutes, and Admin groups with permissions"

    def handle(self, *args, **options):
        # Create groups
        g_student, _ = Group.objects.get_or_create(name="Students")
        g_institute, _ = Group.objects.get_or_create(name="Institutes")
        g_admin, _ = Group.objects.get_or_create(name="Admins")

        # Example: give Institutes permission to add/change/delete OfferedCourse
        ct = ContentType.objects.get_for_model(OfferedCourse)
        perms = Permission.objects.filter(
            content_type=ct,
            codename__in=[
                'add_offeredcourse',
                'change_offeredcourse',
                'delete_offeredcourse'
            ]
        )
        for p in perms:
            g_institute.permissions.add(p)

        self.stdout.write(self.style.SUCCESS("Groups created/updated successfully!"))
