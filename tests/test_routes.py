import json

def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

def test_get_all_book(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2

def test_post_new_book(client):
    # Act
    data = {
        "title": "Prairie Book", 
        "description": "i lurve the grass" 
    }
    response = client.post("/books", json = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201