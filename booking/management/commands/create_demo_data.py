from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.auth import get_user_model
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path
import os

class Command(BaseCommand):
    help = "Create demo data (admin, 3 users, 3 rooms) and export accounts to a PDF."

    def add_arguments(self, parser):
        parser.add_argument(
            "--pdf-name",
            type=str,
            default="user_accounts.pdf",
            help="PDF file name to save account credentials (in BASE_DIR/deploy_reports).",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        accounts = []

        admin_username = "admin"
        admin_password = "admin123"
        if not User.objects.filter(username=admin_username).exists():
            try:
                User.objects.create_superuser(
                    username=admin_username,
                    password=admin_password,
                    email="admin@example.com"
                )
                self.stdout.write(self.style.SUCCESS(f"Created admin: {admin_username}"))
            except TypeError:
                u = User.objects.create(username=admin_username, email="admin@example.com")
                u.set_password(admin_password)
                u.is_staff = True
                u.is_superuser = True
                u.save()
                self.stdout.write(self.style.SUCCESS(f"Created admin (fallback): {admin_username}"))
        else:
            self.stdout.write(self.style.WARNING("Admin already exists"))
        accounts.append((admin_username, admin_password, "admin"))


        users_to_create = [
            ("user1", "user123"),
            ("user2", "user123"),
            ("user3", "user123"),
        ]

        for username, password in users_to_create:
            user_exists = User.objects.filter(username=username).exists()

            if not user_exists:
                User.objects.create_user(username=username, password=password)
                accounts.append((username, password, "user"))
                self.stdout.write(self.style.SUCCESS(f"✅ Created user: {username}"))
            else:
                accounts.append((username, "(already existed)", "user"))
                self.stdout.write(self.style.WARNING(f"⚠️ User {username} already exists"))
        
        Room = apps.get_model('booking', 'Room')  
        room_list = [
            ("Room A", 4, "Demo room A"),
            ("Room B", 8, "Demo room B"),
            ("Room C", 2, "Demo room C"),
        ]
        for name, cap, desc in room_list:
            obj, created = Room.objects.get_or_create(name=name, defaults={'capacity': cap, 'description': desc})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created room: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Room already exists: {name}"))

        
        base_dir = Path(settings.BASE_DIR)
        out_folder = base_dir / "deploy_reports"
        out_folder.mkdir(parents=True, exist_ok=True)
        pdf_name = options['pdf_name']
        pdf_path = out_folder / pdf_name

        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 800, "Demo User Accounts")
        c.setFont("Helvetica", 11)
        y = 770
        for uname, pwd, role in accounts:
            line = f"{role.upper():6} | Username: {uname} | Password: {pwd}"
            c.drawString(50, y, line)
            y -= 18
            if y < 60:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = 800
        c.save()

        self.stdout.write(self.style.SUCCESS(f"Exported accounts PDF to: {pdf_path}"))
        self.stdout.write(self.style.SUCCESS("Done."))
