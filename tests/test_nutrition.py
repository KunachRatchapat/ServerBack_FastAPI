from typing import cast

from db.models.fruit_model import Fruit
from db.models.vegetable_model import Vegetable


def _create_fruit(db) -> int:
    fruit = Fruit(name="Test Fruit", picture="test.jpg", description="Test")
    db.add(fruit)
    db.commit()
    db.refresh(fruit)
    return cast(int, fruit.id)


def _create_vegetable(db) -> int:
    veg = Vegetable(name="Test Veg", picture="test.jpg", description="Test")
    db.add(veg)
    db.commit()
    db.refresh(veg)
    return cast(int, veg.id)


def test_list_nutrition_empty(client):
    r = client.get("/api/v1/nutrition/")
    assert r.status_code == 200
    assert r.json()["result"]["count"] == 0


def test_create_nutrition(client, db, admin_headers):
    fruit_id = _create_fruit(db)
    r = client.post(
        "/api/v1/nutrition/",
        headers=admin_headers,
        json={
            "fruit_id": fruit_id,
            "calories": 100,
            "protein": 2.0,
            "carbs": 20.0,
            "fat": 1.0,
            "fiber": 3.0,
        },
    )
    assert r.status_code == 201
    assert r.json()["result"]["fruit_id"] == fruit_id


def test_create_nutrition_requires_admin(client, db, user_headers):
    fruit_id = _create_fruit(db)
    r = client.post(
        "/api/v1/nutrition/",
        headers=user_headers,
        json={"fruit_id": fruit_id, "calories": 100},
    )
    assert r.status_code == 403


def test_get_nutrition(client, db, admin_headers):
    fruit_id = _create_fruit(db)
    r = client.post(
        "/api/v1/nutrition/",
        headers=admin_headers,
        json={"fruit_id": fruit_id, "calories": 150},
    )
    nid = r.json()["result"]["id"]
    r = client.get(f"/api/v1/nutrition/{nid}")
    assert r.status_code == 200
    assert r.json()["result"]["calories"] == 150


def test_get_nutrition_not_found(client):
    r = client.get("/api/v1/nutrition/9999")
    assert r.status_code == 404


def test_get_nutrition_by_fruit(client, db, admin_headers):
    fruit_id = _create_fruit(db)
    client.post(
        "/api/v1/nutrition/",
        headers=admin_headers,
        json={"fruit_id": fruit_id, "calories": 200},
    )
    r = client.get(f"/api/v1/nutrition/fruit/{fruit_id}")
    assert r.status_code == 200
    assert r.json()["result"]["calories"] == 200


def test_get_nutrition_by_vegetable(client, db, admin_headers):
    veg_id = _create_vegetable(db)
    client.post(
        "/api/v1/nutrition/",
        headers=admin_headers,
        json={"vegetable_id": veg_id, "calories": 80},
    )
    r = client.get(f"/api/v1/nutrition/vegetable/{veg_id}")
    assert r.status_code == 200
    assert r.json()["result"]["calories"] == 80


def test_update_nutrition(client, db, admin_headers):
    fruit_id = _create_fruit(db)
    r = client.post(
        "/api/v1/nutrition/",
        headers=admin_headers,
        json={"fruit_id": fruit_id, "calories": 100},
    )
    nid = r.json()["result"]["id"]
    r = client.put(
        f"/api/v1/nutrition/{nid}",
        headers=admin_headers,
        json={"calories": 999},
    )
    assert r.status_code == 200
    assert r.json()["result"]["calories"] == 999


def test_delete_nutrition(client, db, admin_headers):
    fruit_id = _create_fruit(db)
    r = client.post(
        "/api/v1/nutrition/",
        headers=admin_headers,
        json={"fruit_id": fruit_id, "calories": 100},
    )
    nid = r.json()["result"]["id"]
    r = client.delete(f"/api/v1/nutrition/{nid}", headers=admin_headers)
    assert r.status_code == 204
    r = client.get(f"/api/v1/nutrition/{nid}")
    assert r.status_code == 404
