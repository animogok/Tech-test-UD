"""
This module defines the User database model using SQLAlchemy ORM.

The UserDb class represents a table in the database with fields for user information
such as name, surname, email, age, wallet, hashed_password, date_joined, and is_active.

The model is used for creating, updating, and retrieving user data from the database.
"""

import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from SQL.engine import Base


class UserDb(Base):
    """
    SQLModel for User database table.

    Attributes:
        id (int): Primary key.
        name (str): User's first name.
        surname (str): User's last name.
        email (str): User's email address.
        age (int): User's age.
        wallet (str): User's wallet identifier.
        hashed_password (str): User's hashed password.
        date_joined (datetime): Date and time when the user joined.
        is_active (bool): Status indicating if the user is active.
    """

    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    surname = Column(String(20))
    email = Column(String(50), unique=True, index=True)
    age = Column(Integer)
    wallet = Column(String(20))
    hashed_password = Column(String(50))
    date_joined = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=False)
    # Relación con SportEvent
    events = relationship(
        "SportEvent", back_populates="user", cascade="all, delete-orphan"
    )
    # Relación con Bets
    bets = relationship("Bets", back_populates="user", cascade="all, delete-orphan")


class SportEvent(Base):
    __tablename__ = "Sport_Event"
    id = Column(Integer, primary_key=True)
    event_name = Column(String(50))
    event_final_date = Column(DateTime)
    event_type = Column(String(100))
    team_home = Column(String(50))
    team_away = Column(String(50))
    event_status = Column(Boolean, default=False)
    # Clave foránea a UserDb
    user_email = Column(String(50), ForeignKey("User.email", ondelete="CASCADE"))
    # Relación con UserDb
    user = relationship("UserDb", back_populates="events")
    # Relación con Bets
    bets = relationship("Bets", back_populates="event", cascade="all, delete-orphan")


class Bets(Base):
    __tablename__ = "Bet"
    id = Column(Integer, primary_key=True)
    odd = Column(Float)
    team_home_score_pred = Column(Integer)
    team_away_score_pred = Column(Integer)
    cash = Column(Float)
    # Clave foránea a UserDb
    user_email = Column(String(50), ForeignKey("User.email", ondelete="CASCADE"))
    # Clave foránea a SportEvent
    sport_event_id = Column(Integer, ForeignKey("Sport_Event.id", ondelete="CASCADE"))
    # Relación con UserDb
    user = relationship("UserDb", back_populates="bets")
    # Relación con SportEvent
    event = relationship("SportEvent", back_populates="bets")
