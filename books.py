from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.exceptions import HTTPException
import models
from database import engine, SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class Book(BaseModel):
    id: int
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()

@app.post("/books")
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book_model

@app.put("/{book_id}")
def update_book(book_id: int, in_book: Book, db: Session = Depends(get_db)):

    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} Does not exist"
        )
    book_model.title = in_book.title
    book_model.author = in_book.author
    book_model.description = in_book.description
    book_model.rating = in_book.rating

    db.add(book_model)
    db.commit()

    return book_model

@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} Does not exist"
        )

    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()
    return {"detail": f"Book with ID {book_id} deleted successfully."}