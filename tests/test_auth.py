def test_register(client):
    r = client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser", "password": "Pass1234",
            "email": "new@test.com", "surname": "New",
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert data["code"] == "201"
    assert data["result"]["email"] == "new@test.com"


def test_register_duplicate_email(client, user_token):
    r = client.post(
        "/api/v1/auth/register",
        json={
            "username": "dup", "password": "Pass1234",
            "email": "user@test.com", "surname": "Dup",
        },
    )
    assert r.status_code == 409


def test_login(client, user_token):
    r = client.post("/api/v1/auth/login", json={"email": "user@test.com", "password": "user123"})
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == "200"
    assert "access_token" in data["result"]


def test_login_wrong_password(client):
    r = client.post("/api/v1/auth/login", json={"email": "user@test.com", "password": "wrong"})
    assert r.status_code == 401


def test_logout(client, user_headers):
    r = client.post("/api/v1/auth/logout", headers=user_headers)
    assert r.status_code == 200
    assert r.json()["message"] == "Logout successful"


def test_logout_no_token(client):
    r = client.post("/api/v1/auth/logout")
    assert r.status_code == 401
