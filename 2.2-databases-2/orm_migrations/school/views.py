from django.views.generic import ListView
from django.shortcuts import render
from django.db.models.query import Prefetch

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'

    students_objects = Student.objects.prefetch_related(
        Prefetch('teachers', Teacher.objects.all().order_by('name'))).all().order_by('group', 'name')

    students = [{'name': s.name, 'group': s.group,
                 'teachers': [{'name': t.name, 'subject': t.subject} for t in s.teachers.all()]}
                for s in students_objects]

    context = {'students': students}
    return render(request, template, context)


# Если prefetch_related используется в чистом запросе с .all(), то особых трудностей нет, кол-во запросов снижается до 2
# Если prefetch_related используется с сортировкой .all().order_by('name') или фильтрацией,
# то нужно использовать класс Prefetch и сортировать уже внутри Prefetch:
# Prefetch('teachers', Teacher.objects.all().order_by('name')))
# и вместо s.teachers.all().order_by('name') всё будет работать и упорядочивать правильно просто с s.teachers.all()
# В результате сортировка студентов идёт по группам, по фамилиям студентов в каждой группе
# и по фамилиям учителей у каждого студента
# sql-запросов к таблицам student teachers без Prefetch было 5, c Prefetch 2-запроса.