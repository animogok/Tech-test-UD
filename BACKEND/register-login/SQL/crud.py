"""
This module defines the User database model using SQLAlchemy ORM and
provides utility functions to handle user data in the database.

Classes:
    UserDb: Represents the user table in the database.

Functions:
    get_user: Retrieve a user by email from the database.
    update_user: Update user information in the database.
    post_user: Create a new user in the database.
"""

from typing import Optional
from sqlalchemy.orm import Session
from .models import UserDb

# ========================================== USER =============================================


def get_user(db: Session, user_email: str):
    """
    Retrieve a user by email from the database.

    Args:
        db (Session): Database session.
        user_email (str): Email of the user to retrieve.

    Returns:
        UserDb: The user object if found, None otherwise.
    """
    user = db.query(UserDb).filter(UserDb.email == user_email).first()
    return user


def update_user(
    db: Session,
    current_user: UserDb,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
):
    """
    Update user information in the database.

    Args:
        db (Session): Database session.
        current_user (UserDb): Current user object.
        name (Optional[str], optional): New name. Defaults to None.
        surname (Optional[str], optional): New surname. Defaults to None.
        email (Optional[str], optional): New email. Defaults to None.
        password (Optional[str], optional): New password. Defaults to None.

    Returns:
        UserDb: Updated user object.
    """
    print(current_user.email)
    user = db.query(UserDb).filter(UserDb.email == current_user.email).first()
    if name is not None:
        user.name = name
    if surname is not None:
        user.surname = surname
    if email is not None:
        user.email = email
    if password is not None:
        user.hashed_password = password

    # Commit changes to the database
    db.commit()
    db.refresh(user)
    return user


def post_user(db: Session, user_info: dict):
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        user_info (dict): Dictionary containing user information.

    Returns:
        UserDb: The newly created user object.
    """
    # Create a UserDb instance from the Pydantic User data
    user_db = UserDb(
        name=user_info.get("name"),
        surname=user_info.get("surname"),
        email=user_info.get("email"),
        age=user_info.get("age"),
        wallet=user_info.get("wallet"),  # Ensure wallet is a string
        hashed_password=user_info.get(
            "password"
        ),  # You should ideally hash the password here
        is_active=True,  # Set active status if necessary
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db
