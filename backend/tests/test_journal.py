import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def auth_headers(client: TestClient):
    user_data = {"username": "testuser", "password": "password"}
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/login", data=user_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def test_create_journal(client: TestClient, auth_headers):
    response = client.post(
        "/journal/",
        json={"title": "My Journal", "content": "Journal content", "category": "Test"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Journal"
    assert data["content"] == "Journal content"
    assert data["category"] == "Test"


def test_update_journal(client: TestClient, auth_headers):
    response = client.post(
        "/journal/",
        json={"title": "My Journal", "content": "Journal content", "category": "Test"},
        headers=auth_headers,
    )
    journal_id = response.json()["id"]

    update_response = client.put(
        f"/journal/{journal_id}",
        json={
            "title": "Updated Journal",
            "content": "Updated content",
            "category": "Updated",
        },
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["title"] == "Updated Journal"
    assert updated_data["content"] == "Updated content"
    assert updated_data["category"] == "Updated"


def test_delete_journal(client: TestClient, auth_headers):
    response = client.post(
        "/journal/",
        json={"title": "My Journal", "content": "Journal content", "category": "Test"},
        headers=auth_headers,
    )
    journal_id = response.json()["id"]
    delete_response = client.delete(
        f"/journal/{journal_id}",
        headers=auth_headers,
    )
    assert delete_response.status_code == 204


def test_update_non_existent_journal(client: TestClient, auth_headers):
    response = client.put(
        "/journal/999",
        json={"title": "Updated Journal", "content": "Updated content"},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_unauthorized_update_journal(client: TestClient):
    response = client.put(
        "/journal/1", json={"title": "Updated Journal", "content": "Updated content"}
    )
    assert response.status_code == 401


def test_create_journal_without_auth(client: TestClient):
    response = client.post(
        "/journal/", json={"title": "My Journal", "content": "Journal content"}
    )
    assert response.status_code == 401
