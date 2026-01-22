# core/signals.py
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command


@receiver(post_migrate)
def setup_after_migrate(sender, **kwargs):
    
    if getattr(sender, "name", "") != "core":
        return
    
    call_command("setup_roles")

    if settings.DEBUG:
        call_command("setup_social_login")