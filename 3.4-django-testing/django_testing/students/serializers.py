from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Два дня, Карл! (from django_testing.settings import  MAX_STUDENT_PER_COURSE - это было неверно!!!
# А остальное всё правильно было) Сколько я дебажил-передебажил.
from django.conf import settings

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        if len(value) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(
                f'На курсе уже {settings.MAX_STUDENTS_PER_COURSE} студентов.'
                f'Вы превышаете максимальное кол-во ({settings.MAX_STUDENTS_PER_COURSE} чел).')
        return value
