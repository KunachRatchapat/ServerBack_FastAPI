def test_search_empty(client):
    r = client.get("/api/v1/search/?keyword=xyz")
    assert r.status_code == 200
    assert r.json()["result"] == []


def test_search_fruit(client, admin_headers):
    client.post(
        "/api/v1/fruits/",
        json={"name": "Mango", "picture": "mango.jpg", "description": "Sweet"},
        headers=admin_headers,
    )
    r = client.get("/api/v1/search/?keyword=man")
    assert r.status_code == 200
    assert len(r.json()["result"]) == 1
    assert r.json()["result"][0]["name"] == "Mango"


def test_search_excludes_soft_deleted(client, admin_headers):
    r = client.post(
        "/api/v1/fruits/",
        json={"name": "DeletedFruit", "picture": "df.jpg", "description": "Gone"},
        headers=admin_headers,
    )
    fruit_id = r.json()["result"]["id"]
    r = client.get("/api/v1/search/?keyword=DeletedFruit")
    assert r.status_code == 200
    assert len(r.json()["result"]) == 1
    client.delete(f"/api/v1/fruits/{fruit_id}", headers=admin_headers)
    r = client.get("/api/v1/search/?keyword=DeletedFruit")
    assert r.status_code == 200
    assert r.json()["result"] == []


def test_search_vegetable(client, admin_headers):
    client.post(
        "/api/v1/fruits/",
        json={"name": "Carrot", "picture": "carrot.jpg", "description": "Orange"},
        headers=admin_headers,
    )
    r = client.get("/api/v1/search/?keyword=carrot")
    assert r.status_code == 200
    assert len(r.json()["result"]) == 1
