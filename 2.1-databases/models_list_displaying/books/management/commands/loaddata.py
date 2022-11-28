import json

from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Загрузка данных из файла fixtures/books.json в БД postgres'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('fixtures/books.json', newline='', encoding='utf-8') as file:
            books = list(json.load(file))

        for book in books:
            pk = book['pk']
            b_field = book['fields']
            Book.objects.create(id=pk, name=b_field['name'], author=b_field['author'], pub_date=b_field['pub_date'])