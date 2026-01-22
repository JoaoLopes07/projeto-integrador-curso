import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = "Configura automaticamente Site + SocialApps (Google/GitHub) do django-allauth."

    @transaction.atomic
    def handle(self, *args, **options):
        site_id = int(os.getenv("SITE_ID", getattr(settings, "SITE_ID", 1)))
        domain = os.getenv("SITE_DOMAIN", "127.0.0.1:8000")
        name = os.getenv("SITE_NAME", "Local")

        
        site, _ = Site.objects.update_or_create(
            id=site_id,
            defaults={"domain": domain, "name": name},
        )

        def upsert(provider: str, app_name: str, client_id: str, secret: str):
            if not client_id or not secret:
                self.stdout.write(self.style.WARNING(
                    f"[{provider}] CLIENT_ID/SECRET ausentes no .env — pulando."
                ))
                return

            app, _ = SocialApp.objects.update_or_create(
                provider=provider,
                defaults={
                    "name": app_name,
                    "client_id": client_id,
                    "secret": secret,
                },
            )
            app.sites.add(site)

            self.stdout.write(self.style.SUCCESS(
                f"[{provider}] OK (vinculado ao Site id={site.id})"
            ))

        
        upsert("google", "Google", os.getenv("GOOGLE_CLIENT_ID", ""), os.getenv("GOOGLE_SECRET", ""))
        upsert("github", "GitHub", os.getenv("GITHUB_CLIENT_ID", ""), os.getenv("GITHUB_SECRET", ""))

        self.stdout.write(self.style.SUCCESS("Configuração social finalizada ✅"))
