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

import re
from typing import Optional
from sqlalchemy.orm import Session
from .models import Bets, SportEvent, UserDb
from SQL.engine import SessionLocal

# ========================================== USER =============================================#


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


# =================================== SPORT EVENT =========================#


def get_sport_event(event_id: int):
    db = SessionLocal()
    event = db.query(SportEvent).filter(SportEvent.id == event_id)
    return event


def get_all_sport_events() -> list[SportEvent]:
    """
    Retrieve all sport events from the database.

    Args:
        db (Session): Database session.

    Returns:
        list[SportEvent]: A list of all sport event objects.
    """
    db = SessionLocal()
    return list(db.query(SportEvent).all())


def post_sport_event(event_info: list, user_email: str):
    db = SessionLocal()
    event_db = SportEvent(
        event_name=event_info[0],
        event_final_date=event_info[1],
        event_type=event_info[2],
        team_home=event_info[3],
        team_away=event_info[4],
        user_email=user_email,
    )
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


def update_sport_event(
    event_id: int,
    user_email: str,
    event_name: Optional[str] = None,
    event_type: Optional[str] = None,
    team_home: Optional[str] = None,
    team_away: Optional[str] = None,
):
    db = SessionLocal()

    event_db = (
        db.query(SportEvent)
        .filter(SportEvent.id == event_id, SportEvent.user_email == user_email)
        .first()
    )
    if not event_db:
        return None

    if event_name is not None:
        event_db.event_name = event_name
    if event_type is not None:
        event_db.event_type = event_type
    if team_home is not None:
        event_db.team_home = team_home
    if team_away is not None:
        event_db.team_away = team_away

    db.commit()
    db.refresh(event_db)
    return event_db


def post_bet(bet_info: dict, odd: float) -> Bets:
    """
    Create a new bet in the database.

    Args:
        db (Session): Database session.
        bet_info (dict): Dictionary containing bet information.

    Returns:
        Bets: The newly created bet object.
    """
    db = SessionLocal()

    bet_db = Bets(
        odd=bet_info.get("odd"),
        team_home_score_pred=bet_info.get("team_home_score_pred"),
        team_away_score_pred=bet_info.get("team_away_score_pred"),
        cash=bet_info.get("cash"),
        user_email=bet_info.get("user_email"),
        sport_event_id=bet_info.get("event_id"),
    )
    db.add(bet_db)
    db.commit()
    db.refresh(bet_db)
    return bet_db
