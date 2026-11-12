import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from backend.models import Event, Category, Artist, Venue
from django.utils import timezone
from datetime import timedelta

@pytest.fixture(scope="function")
def api_client():
    yield APIClient()

@pytest.fixture(scope="function")
def user():
    yield User.objects.create_user(
        username="user",
        password="1234",
        email="user@example.com",
    )

@pytest.fixture(scope="function")
def event():
    category = Category.objects.create(name="Концерт")
    artist = Artist.objects.create(name="Ніков")
    venue = Venue.objects.create(name="Палац Спорту", city="Київ", address="Спортивна площа, 1")
    yield Event.objects.create(
        title="Test Event",
        price="500",
        date=timezone.now() + timedelta(days=7),
        category=category,
        artist=artist,
        venue=venue,
    )

@pytest.fixture(autouse=True)
def delete_db_before_test():
    Event.objects.all().delete()

@pytest.fixture(scope="function")
def superuser():
    yield User.objects.create_superuser(
        username="adminuser",
        password="1234",
        email="adminuser@example.com",
    )