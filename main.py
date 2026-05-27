from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db, engine
from models import Book, Base
from schemas import BookCreate, BookUpdate, BookResponse

# Create tables in the database (if they don't exist yet)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Tracker API", version="2.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to Book Tracker API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/books")
def get_books(status: Optional[str] = None):
    if status:
        return [b for b in books_db if b["status"] == status]
    return books_db

@app.get("/books/stats")
def get_stats():
    total = len(books_db)
    reading_count = sum(1 for b in books_db if b["status"] == "reading")
    read_count = sum(1 for b in books_db if b["status"] == "read")
    want_to_read_count = sum(1 for b in books_db if b["status"] == "want_to_read")

    read_books = [b for b in books_db if b["status"] == "read"]
    avg_rating = sum(b["rating"] for b in read_books) / len(read_books) if read_books else 0

    return {
        "total_books": total,
        "reading": reading_count,
        "read": read_count,
        "want_to_read": want_to_read_count,
        "average_rating": avg_rating
    }

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", status_code=201)
def create_book(book: BookCreate):
    global next_id
    new_book = book.model_dump()
    new_book["id"] = next_id
    books_db.append(new_book)
    next_id += 1
    return new_book

@app.put("/books/{book_id}")
def update_book(book_id: int, updates: BookUpdate):
    for book in books_db:
        if book["id"] == book_id:
            if updates.status is not None:
                book["status"] = updates.status
            if updates.rating is not None:
                book["rating"] = updates.rating
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book["id"] == book_id:
            removed_book = books_db.pop(i)
            return {"message": "Book deleted", "book": removed_book}
    raise HTTPException(status_code=404, detail="Book not found")