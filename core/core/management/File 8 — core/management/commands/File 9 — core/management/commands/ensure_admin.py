from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

ADMIN_USERNAME = "Sabawoon"
ADMIN_PASSWORD = "Sabawoon1$"
ADMIN_EMAIL = "sabawoon@marketplace.local"


class Command(BaseCommand):
    help = "Ensure only Sabawoon is admin."

    def handle(self, *args, **options):
        others = User.objects.filter(is_staff=True).exclude(username=ADMIN_USERNAME)
        demoted = 0
        for u in others:
            u.is_staff = False
            u.is_superuser = False
            u.save()
            demoted += 1

        user, created = User.objects.get_or_create(
            username=ADMIN_USERNAME,
            defaults={"email": ADMIN_EMAIL},
        )
        user.email = ADMIN_EMAIL
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(ADMIN_PASSWORD)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created admin: {ADMIN_USERNAME}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Reset password: {ADMIN_USERNAME}"))
        if demoted:
            self.stdout.write(self.style.WARNING(f"Demoted {demoted} other staff."))
