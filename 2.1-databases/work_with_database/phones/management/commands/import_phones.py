import csv

from django.core.management.base import BaseCommand
from phones.models import Phone
from django.template.defaultfilters import slugify


class Command(BaseCommand):
    help = 'Загрузка данных из файла phones.csv в БД postgres'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', newline='', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for row in phones:
            Phone.objects.create(name=row['name'], price=row['price'], image=row['image'],
                                 release_date=row['release_date'], lte_exists=row['lte_exists'],
                                 slug=slugify(row['name']))
