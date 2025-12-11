from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create superuser for Render deployment with custom user model'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = 'admin@example.com'      # o'zingizga qulay email
        username = 'admin'               # o'zingizga qulay username
        password = '#Kd3notyet'  # kuchli parol

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                username=username,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {email}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser with email {email} already exists.'))
