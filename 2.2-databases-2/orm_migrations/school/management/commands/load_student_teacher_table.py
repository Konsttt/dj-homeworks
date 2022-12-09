import json

from django.core.management.base import BaseCommand
from school.models import Teacher, Student, StudentTeacher


class Command(BaseCommand):
    help = 'Заполнение данными новой промежуточной таблицы student_teacher из существующей БД и поля teacher' \
           'Производится один раз после применения миграции 0002_add_m2m_teachers_field' \
           'После этой команды поле teacher из таблицы student можно удалить'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        student_objects = Student.objects.all()
        for student in student_objects:
            StudentTeacher.objects.create(student_id=student.id, teacher_id=student.teacher_id)