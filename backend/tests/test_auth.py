from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register", json={"username": "testuser", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_login_user(client: TestClient):
    user_data = {"username": "testuser", "password": "password"}
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/login", data=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_invalid_login_user(client: TestClient):
    user_data = {"username": "testuser", "password": "password"}
    client.post("/auth/register", json=user_data)
    response = client.post(
        "/auth/login", data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 400


def test_duplicate_user_registration(client: TestClient):
    user_data = {"username": "testuser", "password": "password"}
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400


def test_update_user(client: TestClient):
    original_user_data = {"username": "testuser", "password": "password"}
    updated_user_data = {"username": "usertest", "password": "passphrase"}
    register_response = client.post("/auth/register", json=original_user_data)
    assert register_response.status_code == 200
    login_response = client.post("/auth/login", data=original_user_data)
    assert login_response.status_code == 200
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    update_response = client.put(
        f"/auth/{register_response.json()['id']}",
        json=updated_user_data,
        headers=headers,
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["username"] == updated_user_data["username"]


def test_update_other_user(client: TestClient):
    user_1 = {"username": "testuser", "password": "password"}
    user_2 = {"username": "usertest", "password": "passphrase"}
    register_user_1 = client.post("/auth/register", json=user_1)
    assert register_user_1.status_code == 200
    register_user_2 = client.post("/auth/register", json=user_2)
    assert register_user_2.status_code == 200
    login_user_1_response = client.post("/auth/login", data=user_1)
    assert login_user_1_response.status_code == 200
    headers = {
        "Authorization": f"Bearer {login_user_1_response.json()['access_token']}"
    }
    login_user_2_response = client.post("/auth/login", data=user_2)
    assert login_user_2_response.status_code == 200
    user_2_id = register_user_2.json()["id"]
    update_user_2_response = client.put(
        f"/auth/{user_2_id}",
        json={"username": "updated_user2", "password": "passphrase2"},
        headers=headers,
    )
    assert update_user_2_response.status_code == 403
    data = update_user_2_response.json()
    assert data["detail"] == f"Not authorized to update user {user_2_id}"
