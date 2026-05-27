from database import Base
from sqlalchemy import Column, Integer, String

class Book(Base):
    __tablename__ = "books"

    # Primary key - auto-increments
    id = Column(Integer, primary_key=True, index=True)

    # Book information
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    status = Column(String, default="want_to_read", nullable=False)

    # Rating is optional - can be NULL
    rating = Column(Integer, nullable=True)
