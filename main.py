from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Pydantic models for validation
class BookCreate(BaseModel):
    title: str
    author: str
    status: str = "want_to_read"  # "reading", "read", "want_to_read"
    rating: Optional[int] = None  # 1-5, only if status is "read"

class BookUpdate(BaseModel):
    status: Optional[str] = None
    rating: Optional[int] = None

# In-memory storage
books_db = []
next_id = 1

app = FastAPI(title="Book Tracker API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to Book Tracker API"}

@app.get("/health")
def health():
    return {"status": "ok"}