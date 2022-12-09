import json

from django.core.management.base import BaseCommand
from school.models import Teacher, Student


# Забыл, что loaddata - встроенная функция django :)) Делал сам. Во втором задании вспомнил.
class Command(BaseCommand):
    help = 'Загрузка данных из файла school.json в БД postgres'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('school.json', newline='', encoding='utf-8') as file:
            persons = list(json.load(file))

        for person in persons:
            if person['model'] == 'school.teacher':
                Teacher.objects.create(id=person['pk'], name=person['fields']['name'],
                                       subject=person['fields']['subject'])
            else:
                Student.objects.create(id=person['pk'], name=person['fields']['name'],
                                       teacher_id=person['fields']['teacher'],  # ! _id  :) полчаса дебага и гугления!!
                                       group=person['fields']['group'])