import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Library" in resp.data


def test_books(client):
    resp = client.get("/books")
    assert resp.status_code == 200
    assert b"Clean Code" in resp.data


def test_add_book(client):
    resp = client.post("/add", data={"title": "Test Book", "author": "Tester"},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert b"Test Book" in resp.data


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"