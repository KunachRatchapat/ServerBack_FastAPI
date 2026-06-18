def test_list_vegetables_empty(client):
    r = client.get("/api/v1/vegetables/")
    assert r.status_code == 200
    assert r.json()["result"]["results"] == []


def test_create_vegetable(client, admin_headers):
    r = client.post(
        "/api/v1/vegetables/",
        json={"name": "Carrot", "picture": "carrot.jpg", "description": "Orange carrot"},
        headers=admin_headers,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["result"]["name"] == "Carrot"


def test_create_vegetable_requires_admin(client, user_headers):
    r = client.post(
        "/api/v1/vegetables/",
        json={"name": "Broccoli", "picture": "broccoli.jpg", "description": "Green broccoli"},
        headers=user_headers,
    )
    assert r.status_code == 403


def test_get_vegetable(client, admin_headers):
    create = client.post(
        "/api/v1/vegetables/",
        json={"name": "Lettuce", "picture": "lettuce.jpg", "description": "Green lettuce"},
        headers=admin_headers,
    )
    vid = create.json()["result"]["id"]
    r = client.get(f"/api/v1/vegetables/{vid}")
    assert r.status_code == 200
    assert r.json()["result"]["name"] == "Lettuce"


def test_get_vegetable_not_found(client):
    r = client.get("/api/v1/vegetables/9999")
    assert r.status_code == 404


def test_update_vegetable(client, admin_headers):
    create = client.post(
        "/api/v1/vegetables/",
        json={"name": "Old", "picture": "old.jpg", "description": "Old vegetable"},
        headers=admin_headers,
    )
    vid = create.json()["result"]["id"]
    r = client.put(
        f"/api/v1/vegetables/{vid}",
        json={"name": "New"},
        headers=admin_headers,
    )
    assert r.status_code == 200
    assert r.json()["result"]["name"] == "New"


def test_delete_vegetable(client, admin_headers):
    create = client.post(
        "/api/v1/vegetables/",
        json={"name": "Temp", "picture": "temp.jpg", "description": "Temp"},
        headers=admin_headers,
    )
    vid = create.json()["result"]["id"]
    r = client.delete(f"/api/v1/vegetables/{vid}", headers=admin_headers)
    assert r.status_code == 204
    r2 = client.get(f"/api/v1/vegetables/{vid}")
    assert r2.status_code == 404
