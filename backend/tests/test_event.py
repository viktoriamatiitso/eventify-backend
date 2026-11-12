import pytest
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_get_events_list(api_client, event):
    response = api_client.get("/api/events/", format="json")
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_get_empty_events_list(api_client):
    response = api_client.get("/api/events/", format="json")
    assert response.status_code == 200
    assert len(response.data) == 0

@pytest.mark.django_db
def test_get_event_detail(api_client, event):
    response = api_client.get(f"/api/events/{event.id}/", format="json")
    assert response.status_code == 200
    assert response.data["title"] == event.title

@pytest.mark.django_db
def test_get_invalid_event_detail(api_client):
    response = api_client.get("/api/events/999/", format="json")
    assert response.status_code == 404

@pytest.mark.django_db
def test_create_event(api_client, superuser):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "adminuser", "password": "1234",
        },
        format="json"
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.post(
        "/api/events/",
        {
            "title": "New Event", 
            "price": "300", 
            "date": timezone.now() + timedelta(days=7), 
            "category_id": 1, 
            "artist_id": 1, 
            "venue_id": 1
        },
        format="json"
    )

    assert response.status_code == 201
    assert response.data["title"] == "New Event"

@pytest.mark.django_db
def test_create_event_without_permissions(api_client,user):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "user", "password": "1234",
        },
        format="json"
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.post(
        "/api/events/",
        {
            "title": "New Event", 
            "price": "300", 
            "date": timezone.now() + timedelta(days=7), 
            "category_id": 1, 
            "artist_id": 1, 
            "venue_id": 1
        },
        format="json"
    )

    assert response.status_code == 403

@pytest.mark.django_db
def test_create_event_no_authorization(api_client,superuser):
    response = api_client.post(
        "/api/events/",
        {
            "title": "New Event", 
            "price": "300", 
            "date": timezone.now() + timedelta(days=7), 
            "category_id": 1, 
            "artist_id": 1, 
            "venue_id": 1
        },
        format="json"
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_create_event_with_invalid_data(api_client, superuser):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "adminuser", "password": "1234",
        },
        format="json"
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.post(
        "/api/events/",
        {
            "title": "", 
            "price": "300", 
            "date": timezone.now() - timedelta(days=7), 
            "category_id": 1, 
            "artist_id": 1, 
            "venue_id": 1
        },
        format="json"
    )

    assert response.status_code == 400

@pytest.mark.django_db
def test_update_event(api_client, superuser, event):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "adminuser", "password": "1234",
        },
        format="json"
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.put(
        f"/api/events/{event.id}/",
        {
            "title": "Super Event", 
            "price": "350.00", 
            "date": timezone.now() + timedelta(days=7), 
            "category_id": 1, 
            "artist_id": 1, 
            "venue_id": 1
        },
        format="json"
    )

    assert response.status_code == 200
    assert response.data["title"] == "Super Event"
    assert response.data["price"] == "350.00"

@pytest.mark.django_db
def test_update_invalid_event(api_client, superuser, event):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "adminuser", "password": "1234",
        },
        format="json"
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.put(
        "/api/events/999/",
        {
            "title": "Super Event", 
            "price": "350.00", 
            "date": timezone.now() + timedelta(days=7), 
            "category_id": 1, 
            "artist_id": 1, 
            "venue_id": 1
        },
        format="json"
    )

    assert response.status_code == 404

@pytest.mark.django_db
def test_update_event_without_permissions(api_client, user, event):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "user", "password": "1234",
        },
        format="json"
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.put(
        f"/api/events/{event.id}/",
        {
            "title": "Super Event", 
            "price": "350.00", 
            "date": timezone.now() + timedelta(days=7), 
            "category_id": 1, 
            "artist_id": 1, 
            "venue_id": 1
        },
        format="json"
    )

    assert response.status_code == 403

@pytest.mark.django_db
def test_update_event_no_authorization(api_client, superuser, event):
    response = api_client.put(
        f"/api/events/{event.id}/",
        {
            "title": "Super Event", 
            "price": "350.00", 
            "date": timezone.now() + timedelta(days=7), 
            "category_id": 1, 
            "artist_id": 1, 
            "venue_id": 1
        },
        format="json"
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_delete_event(api_client, superuser, event):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "adminuser", "password": "1234",
        },
        format="json"
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.delete(f"/api/events/{event.id}/", format="json")
    assert response.status_code == 204

@pytest.mark.django_db
def test_delete_invalid_event(api_client, superuser, event):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "adminuser", "password": "1234",
        },
        format="json"
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.delete("/api/events/999/", format="json")
    assert response.status_code == 404

@pytest.mark.django_db
def test_delete_event_withot_permissions(api_client, user, event):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "user", "password": "1234",
        },
        format="json"
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.delete(f"/api/events/{event.id}/", format="json")
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_event_no_authorization(api_client, superuser, event):
    response = api_client.delete(f"/api/events/{event.id}/", format="json")
    assert response.status_code == 401