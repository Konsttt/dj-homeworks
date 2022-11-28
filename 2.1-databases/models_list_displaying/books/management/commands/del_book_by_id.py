from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Удаление записи (книги) по id из базы данных netology_models_list'

    def add_arguments(self, parser):
        parser.add_argument('-id', '--ID', type=int, help='Префикс ID')

    def handle(self, *args, **options):
        pk = options['ID']
        Book.objects.get(id=pk).delete()
