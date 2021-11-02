from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, make_response, request

hagantine_library = Blueprint("hagantine", __name__, url_prefix="/books")
hagantine_authors = Blueprint("authors", __name__, url_prefix="/authors")


# books = [
#     Book(1, "The Marvelous Mrs. Gaysel", "Spunky, New York, and undeniably gay."),
#     Book(2, "Frankgay & Gayce", "Turns out Sal and Robert aren't alone at Club Dorothy."),
#     Book(3, "Gayousts", "A couple inherits a rundown mansion in rural Greenwich Village\
#  only to discover they share ownership with some truly queer neighbors")
# ]

@hagantine_library.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        title_query = request.args.get("title")
        if title_query:
            books = Book.query.filter_by(title=title_query)
        else:
            books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title=request_body["title"], 
                        description=request_body["description"])

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} successfully created, with id {new_book.id}", 201)

@hagantine_library.route("/<id>", methods=["GET"])
def handle_book(id):
    book = Book.query.get(id)
    if book:
        return jsonify({"id": book.id,
                    "title": book.title,
                    "description": book.description
                })
    else:
        return make_response(f"Your book id #{id} was not found", 404)

@hagantine_library.route("/<id>", methods=["PUT"])
def update_a_book(id):
    book = Book.query.get(id)
    request_body = request.get_json()

    if book:
        book.title = request_body["title"]
        book.description = request_body["description"]
        db.session.commit()
        return make_response(f"{book.title} was successfully updated with {book.description=}")
    else:
        title = request_body["title"]
        return make_response(f"Your book id #{id} was not found and {title} could not be updated", 404)

@hagantine_library.route("/<id>", methods=["DELETE"])
def delete_a_book(id):
    book = Book.query.get(id)
    if book: 
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} was successfully deleted")
    else:
        return make_response(f"Your book id #{id} was not found and could not be deleted", 404)

@hagantine_authors.route("", methods=["GET"])
def get_all_authors():
    authors = Author.query.all()
    authors_list = []

    for each_author in authors:
        authors_list.append({
            "author id": each_author.author_id,
            "name": each_author.name 
        })

    return make_response(jsonify(authors_list), 200)

@hagantine_authors.route("", methods=["POST"])
def create_new_author():
    request_body = request.get_json()
    if "name" not in request_body:
        return make_response("Please include author name", 400)
    else:
        author = Author(name=request_body["name"])
        return make_response(f"{author.name} successfully created!", 201)

