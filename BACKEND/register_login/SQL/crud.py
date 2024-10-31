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

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from models.sport_event import Bet, UserSportEvent, calculate_odd
from .models import Bets, SportEvent, UserDb
from SQL.engine import SessionLocal


# ========================================== USER =============================================#


def get_user(db: Session, user_email: str) -> Optional[UserDb]:
    """
    Retrieve a user by email from the database.

    Args:
        db (Session): Database session.
        user_email (str): Email of the user to retrieve.

    Returns:
        UserDb: The user object if found, None otherwise.
    """
    return db.query(UserDb).filter(UserDb.email == user_email).first()


def update_user(
    current_user: UserDb,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    wallet: Optional[int] = None,
) -> UserDb:
    """
    Update user information in the database.

    Args:
        current_user (UserDb): Current user object.
        name (Optional[str], optional): New name. Defaults to None.
        surname (Optional[str], optional): New surname. Defaults to None.
        wallet (Optional[float], optional): New wallet balance. Defaults to None.
        email (Optional[str], optional): New email. Defaults to None.
        password (Optional[str], optional): New password. Defaults to None.

    Returns:
        UserDb: Updated user object.
    """
    db = SessionLocal()
    user = db.query(UserDb).filter(UserDb.email == current_user.email).first()
    if name is not None:
        user.name = name
    if surname is not None:
        user.surname = surname
    if email is not None:
        user.email = email
    if wallet is not None:
        user.wallet = str(wallet + float(user.wallet))  # Update wallet balance
    if password is not None:
        user.hashed_password = password
    db.commit()
    db.refresh(user)  # Refreshes the instance with updated data from the DB
    return user


def post_user(db: Session, user_info: dict) -> UserDb:
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        user_info (dict): Dictionary containing user information.

    Returns:
        UserDb: The newly created user object.
    """
    user_db = UserDb(
        name=user_info.get("name"),
        surname=user_info.get("surname"),
        email=user_info.get("email"),
        age=user_info.get("age"),
        wallet=user_info.get("wallet"),
        hashed_password=user_info.get("password"),  # Hash the password for security
        is_active=True,  # Set active status if necessary
    )
    db.add(user_db)  # Adds the user to the session
    db.commit()  # Commits the transaction
    db.refresh(user_db)  # Retrieves the instance from the DB
    return user_db


# =================================== SPORT EVENT =========================#


def get_sport_event(db: Session, event_id: int) -> Optional[SportEvent]:
    """
    Retrieve a sport event by ID from the database.

    Args:
        event_id (int): ID of the event to retrieve.

    Returns:
        SportEvent: The event object if found, None otherwise.
    """
    return db.query(SportEvent).filter(SportEvent.id == event_id).first()


def get_all_sport_events() -> list[SportEvent]:
    """
    Retrieve all sport events from the database that have a final date after the current date and time.

    Returns:
        list[SportEvent]: A list of all sport event objects with a future final date.
    """
    db: Session = SessionLocal()
    current_time = datetime.now()
    # Query events that are still upcoming
    return db.query(SportEvent).filter(SportEvent.event_final_date > current_time).all()


def post_sport_event(event_info: list, user=str) -> SportEvent:
    """
    Create a new sport event in the database.

    Args:
        event_info (dict): Dictionary containing event information.
        user_email (str): Email of the user creating the event.

    Returns:
        SportEvent: The newly created sport event object.
    """
    db = SessionLocal()
    event_db = SportEvent(
        event_name=event_info[0],
        event_final_date=event_info[1],
        event_type=event_info[2],
        team_home=event_info[3],
        team_away=event_info[4],
        user_email=user,
    )

    db.add(event_db)
    db.commit()
    db.refresh(event_db)

    # Update user's event count
    user_db = get_user(db=db, user_email=user)
    user_db.events_count = user_db.events_count + 1
    db.commit()
    db.refresh(user_db)
    return event_db


def update_sport_event(
    event_id: int,
    user_email: str,
    event_name: Optional[str] = None,
    event_type: Optional[str] = None,
    team_home: Optional[str] = None,
    team_away: Optional[str] = None,
) -> Optional[SportEvent]:
    """
    Update an existing sport event in the database.

    Args:
        event_id (int): ID of the event to be updated.
        user_email (str): Email of the user who owns the event.
        event_name (Optional[str], optional): New name of the event.
        event_type (Optional[str], optional): New type of the event.
        team_home (Optional[str], optional): New home team name.
        team_away (Optional[str], optional): New away team name.

    Returns:
        SportEvent: The updated sport event object, or None if not found.
    """
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


# =============================================== BET ==========================================#


def get_sport_event_bets(event_id: int) -> List[Bet]:
    """
    Retrieve all bets associated with a given sport event ID.

    Args:
        event_id (int): ID of the event.

    Returns:
        List[Bet]: A list of Bet objects associated with the event.
    """
    db = SessionLocal()
    return list(db.query(Bets).filter(Bets.sport_event_id == event_id))


def post_bet(
    event_id: int,
    user_email: str,
    pred1: int,
    pred2: int,
    cash: float,
):
    """
    Place a new bet on a sport event in the database.

    Args:
        event_id (int): ID of the sport event.
        user_email (str): Email of the user placing the bet.
        pred1 (int): Predicted score for the home team.
        pred2 (int): Predicted score for the away team.
        cash (float): Amount of money wagered.

    Returns:
        Bets: The new bet object.
    """
    db = SessionLocal()
    # Calculate the betting odds based on predicted scores
    odd = calculate_odd(home_team_score=pred1, away_team_score=pred2)
    bet_db = Bets(
        odd=odd,
        team_home_score_pred=pred1,
        team_away_score_pred=pred2,
        cash=cash,
        user_email=user_email,
        sport_event_id=event_id,
    )

    db.add(bet_db)
    db.commit()
    db.refresh(bet_db)

    # Update the user's bet count
    user_db = get_user(db=db, user_email=user_email)
    user_db.bets_count = user_db.bets_count + 1
    db.commit()
    db.refresh(user_db)

    # Update the event's bet count
    event_db = get_sport_event(db=db, event_id=event_id)
    event_db.bets_count = event_db.bets_count + 1
    db.commit()
    db.refresh(event_db)

    return bet_db
