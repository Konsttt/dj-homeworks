from random import randint

from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
import pytest

from students.models import Course


@pytest.mark.django_db
def test_one_course_get(client, course_factory, num_records=10):
    courses = course_factory(_quantity=num_records)
    random_course = courses[randint(0, num_records - 1)]
    # Функция reverse работает так: url=reverse(<basename>+'-list')='/api/v1/courses/'
    url = reverse('courses-list') + f'{random_course.id}/'
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert result
    assert result['name'] == random_course.name


@pytest.mark.django_db
def test_list_course_get(client, course_factory, num_records=10):
    courses = course_factory(_quantity=num_records)
    response = client.get('/api/v1/courses/')  # url - без использования reverse
    assert response.status_code == HTTP_200_OK
    resp_json = response.json()
    assert resp_json[0]
    assert len(resp_json) == num_records
    exp_names = [course.name for course in courses]
    res_names = [result['name'] for result in resp_json]
    assert res_names == exp_names


@pytest.mark.django_db
def test_filter_id_get(client, course_factory, num_records=10):
    """
        Тест фильтрации записей таблицы Course по id:
       :param client: APIClient
       :param course_factory: фабрика pytest.fixture
       :num_records: кол-во создаваемых записей course для теста
   """
    courses = course_factory(_quantity=num_records)
    random_course = courses[randint(0, num_records-1)]  # берём случайный созданный объект (курс) из списка
    url = reverse('courses-list')
    response = client.get(url, {'id': random_course.id})
    assert response.status_code == HTTP_200_OK
    resp_json = response.json()
    assert resp_json[0]
    assert len(resp_json) == 1
    assert resp_json[0]['id'] == random_course.id


@pytest.mark.django_db
def test_filter_name_get(client, course_factory, num_records=10):
    courses = course_factory(_quantity=num_records)
    random_course = courses[randint(0, num_records-1)]
    url = reverse('courses-list')
    response = client.get(url, {'name': random_course.name})
    assert response.status_code == HTTP_200_OK
    resp_json = response.json()
    assert resp_json[0]
    # Цикл, т.к. поле name не unique и после фильтра может быть несколько записей
    for course in resp_json:
        assert course['name'] == random_course.name


@pytest.mark.django_db
def test_one_course_create(client, test_name='DRF API course'):
    count = Course.objects.count()
    url = reverse('courses-list')
    response = client.post(url, {'name': test_name})
    assert response.status_code == HTTP_201_CREATED
    assert Course.objects.count() == count + 1
    resp_json = response.json()
    assert resp_json
    assert resp_json['name'] == test_name


@pytest.mark.django_db
def test_course_update(client, course_factory, num_records=10, test_name='DRF API course'):
    courses = course_factory(_quantity=num_records)
    random_course = courses[randint(0, num_records - 1)]
    url = reverse('courses-list') + f'{random_course.id}/'
    response = client.put(url, {'name': test_name})
    assert response.status_code == HTTP_200_OK
    resp_json = response.json()
    assert resp_json
    assert resp_json['name'] == test_name


@pytest.mark.django_db
def test_course_delete(client, course_factory, num_records=10):
    courses = course_factory(_quantity=num_records)
    count = Course.objects.count()
    random_course = courses[randint(0, num_records - 1)]
    url = reverse('courses-list') + f'{random_course.id}/'
    response = client.delete(url)
    assert response.status_code == 204
    assert response.data is None
    assert Course.objects.count() == count - 1


@pytest.mark.django_db
@pytest.mark.parametrize(["max_value", "expected_status"], ((0, HTTP_400_BAD_REQUEST), (1, HTTP_201_CREATED)))
def test_max_student_per_course_create(client, student_factory, max_value, expected_status, settings):
    settings.MAX_STUDENTS_PER_COURSE = max_value
    student1 = student_factory()
    pk1 = student1.id
    url = reverse('courses-list')
    response = client.post(url, {'name': 'course1_name', 'students': [pk1]})
    assert response.status_code == expected_status
