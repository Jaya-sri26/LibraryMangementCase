import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Library" in rv.data
    assert b"Total Books" in rv.data

def test_books_page(client):
    rv = client.get("/books")
    assert rv.status_code == 200
    assert b"All Books" in rv.data

def test_available_page(client):
    rv = client.get("/available")
    assert rv.status_code == 200
    assert b"Available Books" in rv.data

def test_borrowed_page(client):
    rv = client.get("/borrowed")
    assert rv.status_code == 200
    assert b"Borrowed Books" in rv.data

def test_health(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "healthy"
