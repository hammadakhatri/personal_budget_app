from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Neon database URL from environment
NEON_DATABASE_URL = os.getenv("NEON_DB_KEY")

if not NEON_DATABASE_URL:
    raise ValueError("NEON_DB_KEY not found in .env file")

# Create engine for PostgreSQL (Neon)
engine = create_engine(NEON_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def set_user_context(db, user_id: int):
    """Set the user context for Row-Level Security"""
    db.execute(text(f"SET app.user_id = '{user_id}'"))
    db.commit()


