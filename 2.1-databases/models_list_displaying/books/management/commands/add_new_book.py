import datetime

from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Запись одной книги в базу данных netology_models_list'

    def add_arguments(self, parser):
        parser.add_argument('-id', '--ID', type=int, help='Префикс ID')
        parser.add_argument('-n', '--Name', type=str, help='Префикс названия книги')
        parser.add_argument('-a', '--Author', type=str, help='Префикс автора книги')
        parser.add_argument('-d', '--Date', type=str, help='Префикс имени даты публикации')

    def handle(self, *args, **options):
        pk = options['ID']
        name = options['Name']
        author = options['Author']
        pub_date = options['Date']
        Book.objects.create(id=pk, name=name, author=author, pub_date=pub_date)