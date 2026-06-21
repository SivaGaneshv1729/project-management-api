def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert "email" in response.json()
    assert response.json()["email"] == "test@example.com"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()

def test_login_user(client):
    client.post(
        "/api/auth/register",
        json={"email": "test2@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "test2@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
