from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# Create SQLAlchemy engine
# echo=True logs all SQL statements (useful for debugging)
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
# This will be used to create new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for models to inherit from
# All SQLAlchemy models will inherit from this Base class
Base = declarative_base()

# Dependency function for FastAPI
# This yields a database session for each request and ensures it's closed afterwards
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
