from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

ADMIN_USERNAME = "Sabawoon"


@receiver(pre_save, sender=User)
def enforce_single_admin(sender, instance, **kwargs):
    if instance.username == ADMIN_USERNAME:
        instance.is_staff = True
        instance.is_superuser = True
        instance.is_active = True
        return
    if instance.is_staff or instance.is_superuser:
        instance.is_staff = False
        instance.is_superuser = False


@receiver(pre_delete, sender=User)
def protect_admin(sender, instance, **kwargs):
    if instance.username == ADMIN_USERNAME:
        raise ValidationError("The admin account cannot be deleted.")
