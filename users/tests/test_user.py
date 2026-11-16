import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_get_user_info_no_authorization(api_client, user):
    response = api_client.get(f"/api/auth/users/{user.id}/", format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_user_info(api_client, user):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "user",
            "password": "1234",
        },
        format="json",
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.get(f"/api/auth/users/{user.id}/", format="json")
    assert response.status_code == 200
    assert response.data["username"] == user.username


@pytest.mark.django_db
def test_get_invalid_user_info(api_client, user):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "user",
            "password": "1234",
        },
        format="json",
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.get("/api/auth/users/999/", format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_user_info(api_client, user):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "user",
            "password": "1234",
        },
        format="json",
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.put(
        f"/api/auth/users/{user.id}/",
        {
            "username": "user",
            "first_name": "Test User",
            "email": "test_user@example.com",
            "password": "1234",
        },
        format="json",
    )
    assert response.status_code == 200
    assert response.data["first_name"] == "Test User"
    assert response.data["email"] == "test_user@example.com"


@pytest.mark.django_db
def test_update_user_info_no_authorization(api_client, user):
    response = api_client.put(
        f"/api/auth/users/{user.id}/",
        {
            "username": "user",
            "first_name": "Test User",
            "email": "test_user@example.com",
            "password": "1234",
        },
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_invalid_user_info(api_client, user):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "user",
            "password": "1234",
        },
        format="json",
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.put(
        "/api/auth/users/999/",
        {
            "username": "user",
            "first_name": "Test User",
            "email": "test_user@example.com",
            "password": "1234",
        },
        format="json",
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_other_user_info(api_client, user):
    user2 = User.objects.create_user(username="user2", password="1234")
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "user",
            "password": "1234",
        },
        format="json",
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.put(
        f"/api/auth/users/{user2.id}/",
        {
            "username": "user",
            "first_name": "Test User",
            "email": "test_user@example.com",
            "password": "1234",
        },
        format="json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_user_info_with_invalid_data(api_client, user):
    login_url = "/api/auth/login/"
    tokens = api_client.post(
        login_url,
        {
            "username": "user",
            "password": "1234",
        },
        format="json",
    )

    access_token = tokens.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.put(
        f"/api/auth/users/{user.id}/",
        {
            "username": "user",
            "first_name": "Test User",
            "email": "not_an_email",
            "password": "1234",
        },
        format="json",
    )
    assert response.status_code == 400
