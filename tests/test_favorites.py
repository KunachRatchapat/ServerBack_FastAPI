

def test_toggle_favorite(client, admin_headers, user_headers):
    create = client.post(
        "/api/v1/fruits/",
        json={"name": "Apple", "picture": "apple.jpg", "description": "Red apple"},
        headers=admin_headers,
    )
    fid = create.json()["result"]["id"]
    r = client.post(
        "/api/v1/favorites/toggle",
        json={"fruit_id": fid},
        headers=user_headers,
    )
    assert r.status_code == 200
    assert "Favorite Success" in r.json()["message"]


def test_toggle_unfavorite(client, admin_headers, user_headers):
    create = client.post(
        "/api/v1/fruits/",
        json={"name": "Banana", "picture": "banana.jpg", "description": "Yellow"},
        headers=admin_headers,
    )
    fid = create.json()["result"]["id"]
    client.post(
        "/api/v1/favorites/toggle",
        json={"fruit_id": fid},
        headers=user_headers,
    )
    r = client.post(
        "/api/v1/favorites/toggle",
        json={"fruit_id": fid},
        headers=user_headers,
    )
    assert r.status_code == 200
    assert "Unfavorite Success" in r.json()["message"]


def test_list_favorites(client, admin_headers, user_headers):
    create = client.post(
        "/api/v1/fruits/",
        json={"name": "Cherry", "picture": "cherry.jpg", "description": "Sweet"},
        headers=admin_headers,
    )
    fid = create.json()["result"]["id"]
    client.post(
        "/api/v1/favorites/toggle",
        json={"fruit_id": fid},
        headers=user_headers,
    )
    r = client.get("/api/v1/favorites/", headers=user_headers)
    assert r.status_code == 200
    items = r.json()["result"]
    assert len(items) == 1
    assert items[0]["item_name"] == "Cherry"


def test_toggle_favorite_rejects_both_ids(client, admin_headers, user_headers):
    fruit = client.post(
        "/api/v1/fruits/",
        json={"name": "Durian", "picture": "durian.jpg", "description": "Strong"},
        headers=admin_headers,
    )
    veg = client.post(
        "/api/v1/vegetables/",
        json={"name": "Kale", "picture": "kale.jpg", "description": "Green"},
        headers=admin_headers,
    )
    r = client.post(
        "/api/v1/favorites/toggle",
        json={"fruit_id": fruit.json()["result"]["id"], "vegetable_id": veg.json()["result"]["id"]},
        headers=user_headers,
    )
    assert r.status_code == 422


def test_list_favorites_requires_auth(client):
    r = client.get("/api/v1/favorites/")
    assert r.status_code == 401
