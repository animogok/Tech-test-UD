"""
This module defines the User database model using SQLAlchemy ORM.

The UserDb class represents a table in the database with fields for user information
such as name, surname, email, age, wallet, hashed_password, date_joined, and is_active.

The model is used for creating, updating, and retrieving user data from the database.
"""

import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
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
    email = Column(String(50))
    age = Column(Integer)
    wallet = Column(String(20))
    hashed_password = Column(String(50))
    date_joined = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=False)
