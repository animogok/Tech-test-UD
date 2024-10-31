"""
This module provides user authentication functionality, including login and registration systems.
It utilizes FastAPI for creating APIs and JWT for token management.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from SQL.crud import get_user
from SQL.engine import SessionLocal

from .config import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserPublic(BaseModel):
    """
    Represents a public user model without sensitive information.

    Attributes:
        name (str): The user's first name.
        surname (str): The user's last name.
        age (int): The user's age.
        email (EmailStr): The user's email address.
        wallet (int): The user's wallet balance.
    """

    name: str
    surname: str
    age: int
    email: EmailStr
    wallet: int


class User(UserPublic):
    """
    Represents a user model that includes sensitive information.

    Inherits from User_public and adds the following attributes:
        password (str): The user's password (hashed).
        is_active (bool): Indicates whether the user's account is active.

    Config:
        orm_mode (bool): Enables ORM mode to work with SQLAlchemy models.
    """

    password: str
    is_active: bool = False

    class Config:  # pylint: disable=missing-docstring
        orm_mode = True


class Token(BaseModel):
    """
    Represents the structure of a token response.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token (usually "bearer").
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Represents the structure of token data extracted from the JWT.

    Attributes:
        email (EmailStr): The email of the user associated with the token.
    """

    email: EmailStr


# =========================AUTH METHODS==============================================#


def authenticate_user(email: str, password: str) -> bool | User:
    """
    Authenticates a user by checking the provided email and password.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        bool | User: Returns False if authentication fails, otherwise
                    returns the authenticated User object.
    """
    db = SessionLocal()
    user_db = get_user(db=db, user_email=email)
    if not user_db:
        return False
    if not user_db.hashed_password == password:
        return False
    user_db.is_active = True
    db.commit()
    db.refresh(user_db)
    return user_db


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token for the user.

    Args:
        data (dict): The data to encode in the token (e.g., user email).
        expires_delta (timedelta | None): Optional expiration time for the token.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Retrieves the current user based on the provided JWT token.

    Args:
        token (str): The JWT access token provided by the user.

    Raises:
        HTTPException: Raises an exception if the token is invalid or the user cannot be found.

    Returns:
        User: The authenticated User object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    db = SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("email")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except jwt.InvalidTokenError as exc:
        raise credentials_exception from exc
    user = get_user(db=db, user_email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
       Checks if the current user is active.
    Args:
           current_user (User): The authenticated User object.

       Raises:
           HTTPException: Raises an exception if the user is not active.

       Returns: UserDb class
    """
    if current_user.is_active == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
