import os
from django.core.files import File
from django.core.management.base import BaseCommand
from voting.models import Category, Candidate


CANDIDATES = [
    ("Sean Shundi", "sean_shundi.jpg"),
    ("Danielle Makena Mwende", "danielle_mwende.jpg"),
    ("Gerald Kerry Ngore", "gerald_ngore.jpg"),
    ("Bhoke Mwita", "bhoke_mwita.jpg"),
    ("Denis Kipchumba", "denis_kipchumba.jpg"),
]


class Command(BaseCommand):
    help = "Loads the Class Representative candidates and their photos"

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(name="Class Representative")

        photo_folder = os.path.join(os.getcwd(), "candidate_photos")

        for name, filename in CANDIDATES:
            filepath = os.path.join(photo_folder, filename)

            candidate, created = Candidate.objects.get_or_create(
                name=name, category=category
            )

            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    candidate.photo.save(filename, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f"Loaded photo for {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"No photo found for {name} at {filepath}"))

        self.stdout.write(self.style.SUCCESS("Done loading candidates."))