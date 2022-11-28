from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Очистка таблицы books базы данных netology_models_list'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Book.objects.all().delete()