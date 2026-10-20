from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

Base = declarative_base()

@st.cache_resource
def get_engine():
    """
    Create and cache the database engine.
    This ensures we don't recreate the connection pool on every rerun.
    """
    NEON_DATABASE_URL = os.getenv("NEON_DB_KEY")
    if not NEON_DATABASE_URL:
        raise ValueError("NEON_DB_KEY not found in .env file")
    
    return create_engine(NEON_DATABASE_URL, pool_pre_ping=True)

def get_db():
    """
    Generator for database sessions.
    """
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def set_user_context(db, user_id: int):
    """Set the user context for Row-Level Security"""
    db.execute(text(f"SET app.user_id = '{user_id}'"))
    db.commit()
