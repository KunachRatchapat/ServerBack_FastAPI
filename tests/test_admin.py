def test_list_users(client, admin_headers):
    r = client.get("/api/v1/admin/users", headers=admin_headers)
    assert r.status_code == 200
    assert r.json()["result"]["count"] >= 1


def test_list_users_requires_admin(client, user_headers):
    r = client.get("/api/v1/admin/users", headers=user_headers)
    assert r.status_code == 403


def test_get_user(client, admin_headers):
    r = client.get("/api/v1/admin/users/1", headers=admin_headers)
    assert r.status_code == 200
    assert r.json()["result"]["email"] == "admin@test.com"


def test_get_user_not_found(client, admin_headers):
    r = client.get("/api/v1/admin/users/9999", headers=admin_headers)
    assert r.status_code == 404


def test_update_user(client, admin_headers):
    r = client.put(
        "/api/v1/admin/users/1",
        json={"role": "admin"},
        headers=admin_headers,
    )
    assert r.status_code == 200
    assert r.json()["result"]["role"] == "admin"


def test_delete_user(client, admin_headers):
    # Register a temp user
    r = client.post(
        "/api/v1/auth/register",
        json={
            "username": "tempdel",
            "password": "Pass1234",
            "email": "tempdel@test.com",
            "surname": "Del",
        },
    )
    uid = r.json()["result"]["id"]
    r2 = client.delete(f"/api/v1/admin/users/{uid}", headers=admin_headers)
    assert r2.status_code == 204


def test_admin_stats_excludes_soft_deleted(client, admin_headers, db):
    from sqlmodel import select

    from db.models.fruit_model import Fruit

    db.add(Fruit(name="Stats Del Fruit", picture="p.jpg", description="d"))
    db.commit()
    before = client.get("/api/v1/admin/stats", headers=admin_headers).json()["result"]["fruits"]
    fruit = db.exec(select(Fruit).where(Fruit.name == "Stats Del Fruit")).first()
    assert fruit is not None
    client.delete(f"/api/v1/fruits/{fruit.id}", headers=admin_headers)
    after = client.get("/api/v1/admin/stats", headers=admin_headers).json()["result"]["fruits"]
    assert after == before - 1


def test_admin_stats(client, admin_headers, db):
    from db.models.fruit_model import Fruit

    db.add(Fruit(name="Stats Fruit", picture="p.jpg", description="d"))
    db.commit()
    r = client.get("/api/v1/admin/stats", headers=admin_headers)
    assert r.status_code == 200
    data = r.json()["result"]
    assert "users" in data
    assert "fruits" in data
    assert "vegetables" in data
    assert "favorites" in data
    assert "nutrition_records" in data
    assert data["fruits"] >= 1


def test_admin_stats_requires_admin(client, user_headers):
    r = client.get("/api/v1/admin/stats", headers=user_headers)
    assert r.status_code == 403
