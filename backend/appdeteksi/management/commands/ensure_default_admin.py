from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Ensure the default admin and staff accounts exist with known credentials.'

    def handle(self, *args, **options):
        User = get_user_model()

        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@retinadetect.local',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        else:
            admin_user.email = 'admin@retinadetect.local'
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password('admin123')
            admin_user.save()

        staff_user, created = User.objects.get_or_create(
            username='jolie@eyedetect.com',
            defaults={
                'email': 'jolie@eyedetect.com',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            staff_user.set_password('staff123')
            staff_user.save()
        else:
            staff_user.email = 'jolie@eyedetect.com'
            staff_user.is_staff = True
            staff_user.is_superuser = True
            staff_user.set_password('staff123')
            staff_user.save()

        self.stdout.write(self.style.SUCCESS('Ensured default admin/staff accounts.'))
