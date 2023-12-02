import csv
from django.core.management.base import BaseCommand
from book_api.models import Book


class Command(BaseCommand):
    help = 'Import data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            # next(reader)  # Skip the header row if it exists

            for row in reader:
                title, author, publication_year = row
                Book.objects.create(title=title, author=author, publication_year=publication_year)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {csv_file_path} into the database.'))
