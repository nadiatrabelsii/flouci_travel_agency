from django.core.management.base import BaseCommand
from travel_app.models import TravelPackage

class Command(BaseCommand):
    help = 'Loads initial travel packages into the database'

    def handle(self, *args, **options):
        packages = [
            {"name": "Beach Paradise", "price": 500, "description": "Sunny beaches", "themes": ["beach", "relax"]},
            {"name": "Mountain Retreat", "price": 300, "description": "Peaceful mountains", "themes": ["nature", "adventure"]},
        ]
        for package_data in packages:
            package, created = TravelPackage.objects.get_or_create(**package_data)
            if created:
                self.stdout.write(f'Package "{package.name}" created.')
            else:
                self.stdout.write(f'Package "{package.name}" already exists.')
