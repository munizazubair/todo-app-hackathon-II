"""
Database connection and session management.
"""
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import QueuePool
from typing import Generator
from core.config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)


def get_engine():
    """
    Get the database engine instance.

    Returns:
        Engine: SQLAlchemy engine instance
    """
    return engine


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection.

    Yields:
        Session: SQLModel session instance

    Usage:
        from fastapi import Depends
        from db.database import get_session

        @app.get("/items")
        def read_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Create database tables from SQLModel models.

    Note: In production, use Alembic migrations instead.
    This function is useful for development and testing.
    """
    SQLModel.metadata.create_all(engine)


def dispose_engine():
    """
    Dispose of the database engine and close all connections.

    This should be called on application shutdown.
    """
    engine.dispose()
