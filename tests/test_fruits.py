

def test_list_fruits_empty(client):
    r = client.get("/api/v1/fruits/")
    assert r.status_code == 200
    assert r.json()["result"]["results"] == []


def test_create_fruit(client, admin_headers):
    r = client.post(
        "/api/v1/fruits/",
        json={"name": "Apple", "picture": "apple.jpg", "description": "Red apple"},
        headers=admin_headers,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["result"]["name"] == "Apple"


def test_create_fruit_requires_admin(client, user_headers):
    r = client.post(
        "/api/v1/fruits/",
        json={"name": "Banana", "picture": "banana.jpg", "description": "Yellow banana"},
        headers=user_headers,
    )
    assert r.status_code == 403


def test_get_fruit(client, admin_headers):
    create = client.post(
        "/api/v1/fruits/",
        json={"name": "Pear", "picture": "pear.jpg", "description": "Green pear"},
        headers=admin_headers,
    )
    fid = create.json()["result"]["id"]
    r = client.get(f"/api/v1/fruits/{fid}")
    assert r.status_code == 200
    assert r.json()["result"]["name"] == "Pear"


def test_get_fruit_not_found(client):
    r = client.get("/api/v1/fruits/9999")
    assert r.status_code == 404


def test_update_fruit(client, admin_headers):
    create = client.post(
        "/api/v1/fruits/",
        json={"name": "Old", "picture": "old.jpg", "description": "Old fruit"},
        headers=admin_headers,
    )
    fid = create.json()["result"]["id"]
    r = client.put(
        f"/api/v1/fruits/{fid}",
        json={"name": "New"},
        headers=admin_headers,
    )
    assert r.status_code == 200
    assert r.json()["result"]["name"] == "New"


def test_delete_fruit(client, admin_headers):
    create = client.post(
        "/api/v1/fruits/",
        json={"name": "Temp", "picture": "temp.jpg", "description": "Temp"},
        headers=admin_headers,
    )
    fid = create.json()["result"]["id"]
    r = client.delete(f"/api/v1/fruits/{fid}", headers=admin_headers)
    assert r.status_code == 204
    r2 = client.get(f"/api/v1/fruits/{fid}")
    assert r2.status_code == 404
