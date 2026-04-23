import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Create or update an admin (superuser) account using environment variables. "
        "Required: ADMIN_EMAIL, ADMIN_PASSWORD. "
        "Optional: ADMIN_USERNAME (defaults to email), ADMIN_FIRST_NAME, ADMIN_LAST_NAME."
    )

    def handle(self, *args, **options):
        from library.models import User

        email = os.environ.get("ADMIN_EMAIL", "").strip()
        password = os.environ.get("ADMIN_PASSWORD", "").strip()

        if not email or not password:
            self.stderr.write(
                self.style.ERROR(
                    "ADMIN_EMAIL and ADMIN_PASSWORD environment variables are required."
                )
            )
            return

        username = os.environ.get("ADMIN_USERNAME", email).strip()
        first_name = os.environ.get("ADMIN_FIRST_NAME", "").strip()
        last_name = os.environ.get("ADMIN_LAST_NAME", "").strip()
        role = os.environ.get("ADMIN_ROLE", "librarian").strip()

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
            },
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True

        if not created:
            user.username = username
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name

        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} admin user: {email}"))
