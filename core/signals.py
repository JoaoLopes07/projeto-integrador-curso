# core/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command


@receiver(post_migrate)
def setup_roles_after_migrate(sender, **kwargs):
    call_command("setup_roles")
