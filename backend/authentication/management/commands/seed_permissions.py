# authentication/management/commands/seed_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from authentication.models import Permission
from typing import Any

class Command(BaseCommand):
    help = 'Seed the database with authentication permission data'

    def handle(self, *args: Any, **kwargs: Any) -> None:
        self.stdout.write(self.style.SUCCESS('Seeding data...'))
        self.create_permissions()
        self.stdout.write(self.style.SUCCESS('Seeding complete.'))

    def create_permissions(self) -> None:
        models_permissions = {
            "account": ["change_account", "view_account"],
            "permission": ["view_permission"],
            "user": ["add_user", "change_user", "delete_user", "view_user"],
            "group": ["add_group", "change_group", "delete_group", "view_group"],
        }

        for model, codenames in models_permissions.items():
            content_type = ContentType.objects.get(app_label='authentication', model=model)
            for codename in codenames:
                name = f"Can {codename.split('_')[0]} {model}"
                permission, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=content_type,
                    defaults={'name': name}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created permission: {name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Permission already exists: {name}'))
