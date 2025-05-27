from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID
from fastapi.exceptions import HTTPException

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)

BOOKS = []

@app.get("/")
def read_api():
    return BOOKS

@app.post("/books")
def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
def update_book(book_id: UUID, in_book: Book):
    counter = 0

    for book in BOOKS:
        counter += 1
        if book.id == book_id:
            BOOKS[counter - 1] = in_book
            return BOOKS[counter - 1]
    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} Does not exist"
    )

@app.delete("/{book_id}")
def delete_book(book_id: UUID):
    counter = 0

    for book in BOOKS:
        counter += 1
        if book.id == book_id:
            del BOOKS[counter - 1]
            return f"ID {book_id} deleted"
    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} Does not exist"
    )