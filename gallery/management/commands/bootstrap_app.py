import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from sklearn.datasets import load_iris
from gallery.models import IrisSample


class Command(BaseCommand):
    help = "Create/ensure admin user, writer role, and seed iris dataset"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-password",
            action="store_true",
            help="Reset admin password even if the user already exists",
        )

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        password = os.environ.get("ADMIN_PASSWORD") or "admin"

        with transaction.atomic():
            admin_user = self._ensure_admin_user(username, email, password, options["reset_password"])
            writer_group = self._ensure_writer_group()
            if not admin_user.groups.filter(name=writer_group.name).exists():
                admin_user.groups.add(writer_group)
                self.stdout.write(self.style.SUCCESS(f"Added '{username}' to '{writer_group.name}' group"))
            self._seed_iris_samples()

        self.stdout.write(self.style.SUCCESS("Bootstrap completed"))

    def _ensure_admin_user(self, username, email, password, reset_password):
        User = get_user_model()
        admin_user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )

        updated = False
        if created:
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password(password)
            updated = True
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'"))
        else:
            if not admin_user.is_staff or not admin_user.is_superuser:
                admin_user.is_staff = True
                admin_user.is_superuser = True
                updated = True
            if reset_password:
                admin_user.set_password(password)
                updated = True
            if email and admin_user.email != email:
                admin_user.email = email
                updated = True

        if updated:
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"Ensured superuser '{username}' (updated={updated})"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already up to date"))

        return admin_user

    def _ensure_writer_group(self):
        writer_group, created = Group.objects.get_or_create(name="writer")
        if created:
            self.stdout.write(self.style.SUCCESS("Created group 'writer'"))
        else:
            self.stdout.write(self.style.SUCCESS("Group 'writer' already exists"))
        return writer_group

    def _seed_iris_samples(self):
        data = load_iris()
        species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}

        created_or_updated = 0
        for idx, (features, label) in enumerate(zip(data.data, data.target), start=1):
            IrisSample.objects.update_or_create(
                instance_id=idx,
                defaults={
                    "sepal_length": float(features[0]),
                    "sepal_width": float(features[1]),
                    "petal_length": float(features[2]),
                    "petal_width": float(features[3]),
                    "species": species_map[label],
                },
            )
            created_or_updated += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created_or_updated} iris samples"))
