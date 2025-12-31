from django.core.management.base import BaseCommand
from app.files.service import load_data

class Command(BaseCommand):
    help = 'Import data from Excel'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        path = options['file_path']
        self.stdout.write(f"Loading {path}...")
        load_data(path)
        self.stdout.write(self.style.SUCCESS("Successful"))