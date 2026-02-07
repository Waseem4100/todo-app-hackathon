from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for testing, PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_test.db")

if "postgres" in DATABASE_URL.lower():
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300,
    )
else:
    # For SQLite, use a simpler engine configuration
    engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    from sqlmodel import Session
    with Session(engine) as session:
        yield session