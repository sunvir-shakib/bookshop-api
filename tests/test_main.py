from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_get_all_books():
    response = client.get("/books")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_single_book():
    response = client.get("/books/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_nonexistent_book():
    response = client.get("/books/999")

    assert response.status_code == 404


def test_create_book():
    new_book = {
        "id": 10,
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "price": 4500,
        "quantity": 7
    }

    response = client.post("/books", json=new_book)

    assert response.status_code == 201
    assert response.json()["title"] == "Introduction to Algorithms"


def test_create_duplicate_book():
    new_book = {
        "id": 1,
        "title": "Another Book",
        "author": "Another Author",
        "price": 2000,
        "quantity": 5
    }

    response = client.post("/books", json=new_book)

    assert response.status_code == 400


def test_update_book():
    updated_book = {
        "id": 1,
        "title": "Python Crash Course Updated",
        "author": "Eric Matthes",
        "price": 2800,
        "quantity": 15
    }

    response = client.put("/books/1", json=updated_book)

    assert response.status_code == 200
    assert response.json()["title"] == "Python Crash Course Updated"


def test_update_nonexistent_book():
    updated_book = {
        "id": 999,
        "title": "Unknown",
        "author": "Unknown",
        "price": 1000,
        "quantity": 1
    }

    response = client.put("/books/999", json=updated_book)

    assert response.status_code == 404


def test_delete_book():
    response = client.delete("/books/2")

    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"


def test_delete_nonexistent_book():
    response = client.delete("/books/999")

    assert response.status_code == 404