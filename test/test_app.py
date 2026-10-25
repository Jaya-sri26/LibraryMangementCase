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
    # Make sure this matches exactly what is in your index.html
    assert b"Total Books" in rv.data 
    assert b"Borrowed Books" in rv.data

def test_books_page(client):
    rv = client.get("/books")
    assert rv.status_code == 200
    assert b"All Books" in rv.data
