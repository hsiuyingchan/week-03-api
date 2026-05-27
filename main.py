from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

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

@app.get("/books", response_model=List[BookResponse])
def get_books(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if status:
        query = query.filter(Book.status == status)
    return query.all()

@app.get("/books/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Book.id)).scalar()
    reading_count = db.query(func.count(Book.id)).filter(Book.status == "reading").scalar()
    read_count = db.query(func.count(Book.id)).filter(Book.status == "read").scalar()
    want_to_read_count = db.query(func.count(Book.id)).filter(Book.status == "want_to_read").scalar()

    read_books = db.query(Book).filter(Book.status == "read").all()
    avg_rating = sum(b.rating for b in read_books if b.rating) / len(read_books) if read_books else 0

    return {
        "total_books": total,
        "reading": reading_count,
        "read": read_count,
        "want_to_read": want_to_read_count,
        "average_rating": avg_rating
    }

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updates: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if updates.status is not None:
        book.status = updates.status
    if updates.rating is not None:
        book.rating = updates.rating
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted", "book": book}
