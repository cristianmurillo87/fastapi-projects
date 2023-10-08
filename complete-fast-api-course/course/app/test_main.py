from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_all_blogs():
    response = client.get("/blog/all")
    assert response.status_code == 200


def test_auth_error():
    response = client.post("/token", data={"username": "", "password": ""})
    access_token = response.json().get("access_token")
    assert access_token == None
    message = response.json().get("detail")[0].get("msg")
    assert message == "field required"


def test_create_user():
    response = client.post(
        "/user", json={"username": "cat2", "password": "cat2", "email": "cat2@email.com"}
    )
    user = response.json()
    username = user.get("username")
    assert username == "cat2"


def test_auth_success():
    auth = client.post("/token", data={"username": "cat", "password": "cat"})
    access_token = auth.json().get("access_token")
    assert access_token


def test_post_article():
    auth = client.post("/token", data={"username": "cat", "password": "cat"})
    access_token = auth.json().get("access_token")
    assert access_token

    response = client.post(
        "/article/",
        json={
            "title": "Test article",
            "content": "Test content",
            "published": True,
            "creator_id": 1,
        },
        headers={"Authorization": f"bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json().get("title") == "Test article"
