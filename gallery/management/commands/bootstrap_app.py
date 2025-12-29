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
        reset_password = options["reset_password"]

        with transaction.atomic():
            admin_user = self.create_admin_user(username, email, password, reset_password)
            writer_group = self.create_writer_group()
            
            # Admin'i 'writer' (yazar) grubuna ekle
            if not admin_user.groups.filter(name=writer_group.name).exists():
                admin_user.groups.add(writer_group)
                self.stdout.write(self.style.SUCCESS(f"Added '{username}' to '{writer_group.name}' group"))
            
            self.create_iris_data()

        self.stdout.write(self.style.SUCCESS("Bootstrap completed"))

    def create_admin_user(self, username, email, password, reset_password):
        User = get_user_model()
        # Kullanıcıyı almaya çalış veya yoksa oluştur
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
            # Kullanıcı mevcut, güncellememe gerek olup olmadığını kontrol et
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
            self.stdout.write(self.style.SUCCESS(f"Ensured superuser '{username}'"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already up to date"))

        return admin_user

    def create_writer_group(self):
        writer_group, created = Group.objects.get_or_create(name="writer")
        if created:
            self.stdout.write(self.style.SUCCESS("Created group 'writer'"))
        else:
            self.stdout.write(self.style.SUCCESS("Group 'writer' already exists"))
        return writer_group

    def create_iris_data(self):
        data = load_iris()
        species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}

        count = 0
        # Veri ve hedefi birleştir
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
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {count} iris samples"))
