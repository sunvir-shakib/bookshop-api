from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="BookShop API")


class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float
    quantity: int


books = [
    Book(
        id=1,
        title="Python Crash Course",
        author="Eric Matthes",
        price=2500,
        quantity=10
    ),
    Book(
        id=2,
        title="Clean Code",
        author="Robert C. Martin",
        price=3000,
        quantity=5
    )
]


# GET - Get all books
@app.get("/books")
def get_books():
    return books


# GET - Get one book
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# POST - Add a new book
@app.post("/books", status_code=201)
def create_book(book: Book):
    for existing_book in books:
        if existing_book.id == book.id:
            raise HTTPException(
                status_code=400,
                detail="Book ID already exists"
            )

    books.append(book)

    return book


# PUT - Update a book
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id and updated_book.id == book_id:
            books[index] = updated_book
            return updated_book

    raise HTTPException(
        status_code=404,
        detail="Book not found or book ID mismatch"
    )


# DELETE - Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted_book = books.pop(index)
            return {
                "message": "Book deleted successfully",
                "book": deleted_book
            }

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )