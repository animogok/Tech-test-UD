"""
This module initializes the FastAPI application, sets up database connections,
and includes user authentication routes.

Functions:
    get_db: Provides a database session for dependency injection.
    read_root: Returns a welcome message.
"""

from fastapi import FastAPI
from routers.user_auth import authentication_user
from routers.user_sport_event import sport_router
from SQL import models
from SQL.engine import SessionLocal, engine

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency to provide a database session.

    Yields:
        db (SessionLocal): Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize the FastAPI application
app = FastAPI()

# Include the authentication routes
app.include_router(authentication_user)
app.include_router(sport_router)


@app.get("/")
async def read_root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: hint.
    """
    return {"detail": "This is the square root :D"}
