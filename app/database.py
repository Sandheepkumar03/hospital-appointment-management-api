"""Database configuration for the Hospital Appointment Management API."""
#pylint: disable=too-few-public-methods

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./hospital.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SESSION_LOCAL = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


def get_db():
    """Provide a database session for API requests."""
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()
