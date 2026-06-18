from datetime import datetime

from sqlmodel import select

from db.models.user_model import Users


def test_register_unverified_cannot_login(client):
    r = client.post(
        "/api/v1/auth/register",
        json={
            "username": "unverified", "password": "Pass1234",
            "email": "unver@test.com", "surname": "Unver",
        },
    )
    assert r.status_code == 201
    r = client.post("/api/v1/auth/login", json={"email": "unver@test.com", "password": "Pass1234"})
    assert r.status_code == 403


def test_verify_email(client, db):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "vuser", "password": "Pass1234",
            "email": "vuser@test.com", "surname": "Vuser",
        },
    )
    user = db.exec(select(Users).where(Users.email == "vuser@test.com")).first()
    token = user.verify_token
    assert token is not None
    r = client.post("/api/v1/auth/verify-email", json={"token": token})
    assert r.status_code == 200
    r = client.post("/api/v1/auth/login", json={"email": "vuser@test.com", "password": "Pass1234"})
    assert r.status_code == 200


def test_verify_email_invalid_token(client):
    r = client.post("/api/v1/auth/verify-email", json={"token": "bogus-token"})
    assert r.status_code == 400


def test_forgot_password(client, db):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "fpuser", "password": "Pass1234",
            "email": "fpuser@test.com", "surname": "FP",
        },
    )
    user = db.exec(select(Users).where(Users.email == "fpuser@test.com")).first()
    token = user.verify_token
    client.post("/api/v1/auth/verify-email", json={"token": token})
    r = client.post("/api/v1/auth/forgot-password", json={"email": "fpuser@test.com"})
    assert r.status_code == 200
    db.expire_all()
    user = db.exec(select(Users).where(Users.email == "fpuser@test.com")).first()
    reset_token = user.reset_token
    assert reset_token is not None
    body = {"token": reset_token, "new_password": "NewPass5678"}
    r = client.post("/api/v1/auth/reset-password", json=body)
    assert r.status_code == 200
    body = {"email": "fpuser@test.com", "password": "NewPass5678"}
    r = client.post("/api/v1/auth/login", json=body)
    assert r.status_code == 200
    r = client.post("/api/v1/auth/login", json={"email": "fpuser@test.com", "password": "Pass1234"})
    assert r.status_code == 401


def test_reset_password_invalid_token(client):
    body = {"token": "bogus", "new_password": "NewPass5678"}
    r = client.post("/api/v1/auth/reset-password", json=body)
    assert r.status_code == 400


def test_reset_password_expired_token(client, db):
    from app.core.security import hash_password
    user = Users(
        email="expired@test.com",
        password=hash_password("Pass1234"),
        username="expired",
        surname="Exp",
        role="user",
        is_verified=True,
        reset_token="expired-token",
        reset_token_expires=datetime(2020, 1, 1),
    )
    db.add(user)
    db.commit()
    body = {"token": "expired-token", "new_password": "NewPass5678"}
    r = client.post("/api/v1/auth/reset-password", json=body)
    assert r.status_code == 400


def test_soft_deleted_user_cannot_login(client, db, admin_headers, user_headers):
    user = db.exec(select(Users).where(Users.email == "user@test.com")).first()
    assert user is not None
    r = client.delete(f"/api/v1/admin/users/{user.id}", headers=admin_headers)
    assert r.status_code == 204
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "user@test.com", "password": "user123"},
    )
    assert r.status_code == 401


def test_soft_deleted_user_token_rejected(client, db, admin_headers, user_headers):
    user = db.exec(select(Users).where(Users.email == "user@test.com")).first()
    assert user is not None
    r = client.get("/api/v1/favorites/", headers=user_headers)
    assert r.status_code == 200
    r = client.delete(f"/api/v1/admin/users/{user.id}", headers=admin_headers)
    assert r.status_code == 204
    r = client.get("/api/v1/favorites/", headers=user_headers)
    assert r.status_code == 401


def test_refresh_token(client, user_token):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "user@test.com", "password": "user123"},
    )
    assert r.status_code == 200
    refresh = r.json()["result"]["refresh_token"]
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
    assert r.status_code == 200
    assert "access_token" in r.json()["result"]
    assert "refresh_token" in r.json()["result"]


def test_refresh_invalid_token(client):
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": "not-a-valid-token"})
    assert r.status_code == 401


def test_refresh_access_token_rejected(client, user_token):
    r = client.post("/api/v1/auth/login", json={"email": "user@test.com", "password": "user123"})
    access = r.json()["result"]["access_token"]
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": access})
    assert r.status_code == 401


def test_refresh_rejects_soft_deleted_user(client, db, admin_headers, user_headers, user_token):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "user@test.com", "password": "user123"},
    )
    refresh = r.json()["result"]["refresh_token"]
    user = db.exec(select(Users).where(Users.email == "user@test.com")).first()
    assert user is not None
    client.delete(f"/api/v1/admin/users/{user.id}", headers=admin_headers)
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
    assert r.status_code == 401


def test_forgot_password_rate_limit(client, monkeypatch):
    from app.config import settings
    from app.core.rate_limit import limiter

    monkeypatch.setattr(limiter, "enabled", True)
    limit = int(settings.RATE_LIMIT.split("/")[0])
    for _ in range(limit):
        r = client.post("/api/v1/auth/forgot-password", json={"email": "nobody@test.com"})
        assert r.status_code == 200
    r = client.post("/api/v1/auth/forgot-password", json={"email": "nobody@test.com"})
    assert r.status_code == 429


def test_change_password(client, user_headers):
    r = client.post(
        "/api/v1/auth/change-password",
        headers=user_headers,
        json={"current_password": "user123", "new_password": "NewPass5678"},
    )
    assert r.status_code == 200
    body = {"email": "user@test.com", "password": "NewPass5678"}
    r = client.post("/api/v1/auth/login", json=body)
    assert r.status_code == 200
    body = {"email": "user@test.com", "password": "user123"}
    r = client.post("/api/v1/auth/login", json=body)
    assert r.status_code == 401
