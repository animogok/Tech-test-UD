from datetime import timedelta
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from models.config import ACCESS_TOKEN_EXPIRE_MINUTES
from models.user import (
    Token,
    User,
    UserPublic,
    active_user,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from SQL.engine import SessionLocal
from SQL.crud import get_user, post_user, update_user


# Create an APIRouter instance
authentication_user = APIRouter()


@authentication_user.post("/token", response_model=Token)
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Handle user login and token generation.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data with username and password.

    Returns:
        Token: JWT access token.

    Raises:
        HTTPException: If authentication fails.
    """
    user = authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email, "wallet": user.wallet},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@authentication_user.post("/sign-up/")
async def register(data: User) -> dict:
    """
    Handle user registration.

    Args:
        data (User): User data for registration.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If email is already used or age is invalid.
    """
    if get_user(db=SessionLocal(), user_email=data.email):
        raise HTTPException(status_code=400, detail="This email has been used before")
    elif (data.age <= 18) or (data.age > 100):
        raise HTTPException(status_code=400, detail="You must be +18 years old")
    else:
        post_user(db=SessionLocal(), user_info=dict(data))
        return {"Success": "User has been created correctly"}


# ====================================== USER CONFIG ======================================


@authentication_user.get("/user-options/", response_model=UserPublic)
async def option(current_user: Annotated[User, Depends(active_user)]):
    """
    Retrieve current user options.

    Args:
        current_user (User): Current authenticated user.

    Returns:
        UserPublic: Public user information.
    """
    return current_user


@authentication_user.post("/user-options/change-values/")
async def option_change_values(
    current_user: Annotated[UserPublic, Depends(option)],
    name: Optional[str] = None,
    surname: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    wallet: Optional[float] = None,
):
    """
    Handle user information update.

    Args:
        current_user (UserPublic): Current authenticated user.
        name (str, optional): New name. Defaults to None.
        surname (str, optional): New surname. Defaults to None.
        email (str, optional): New email. Defaults to None.
        password (str, optional): New password. Defaults to None.

    Returns:
        dict: Updated user information and success message.

    Raises:
        HTTPException: If user is not logged in.
    """
    if current_user is not None:
        updated_user = update_user(
            current_user=current_user,
            name=name,
            surname=surname,
            email=email,
            password=password,
            wallet=wallet,
        )
        return {
            "msg": "User information updated successfully",
            "updated_user": {
                "name": updated_user.name,
                "surname": updated_user.surname,
                "email": updated_user.email,
                "wallet": updated_user.wallet,
            },
        }
    else:
        raise HTTPException(status_code=401, detail="You're not logged in")
