import pytest
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user('except')


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_GetCourse_Api(client, user, courses_factory):
    courses = courses_factory(_quantity=1)
    response = client.get('/api/v1/courses/' + str(courses[0].id) + '/')
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == courses[0].name


@pytest.mark.django_db
def test_GetCourses_api(client, user, courses_factory):
    courses = courses_factory(_quantity=2)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_SearchIdCourses_api(client, user, courses_factory):
    courses = courses_factory(_quantity=5)
    response = client.get('/api/v1/courses/',
                          data={'id': courses[0].id})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == courses[0].id


@pytest.mark.django_db
def test_SearchNameCourses_api(client, user, courses_factory):
    courses = courses_factory(_quantity=5)
    response = client.get('/api/v1/courses/',
                          data={'name': courses[3].name})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == courses[3].name


@pytest.mark.django_db
def test_CreateCourses_api(client, user, courses_factory):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/',
                           data={'name': 'test_course'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_UpdateCourses_api(client, user, courses_factory):
    courses = courses_factory(_quantity=1)
    response = client.patch('/api/v1/courses/' + str(courses[0].id) + '/',
                            data={'name': 'test_course'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_DeleteCourses_api(client, user, courses_factory):
    courses = courses_factory(_quantity=1)
    count = Course.objects.count()
    response = client.delete('/api/v1/courses/' + str(courses[0].id) + '/')
    assert response.status_code == 204
    assert Course.objects.count() == count - 1


