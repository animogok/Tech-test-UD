import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from SQL.engine import Base


class UserDb(Base):
    """SQLModel for User database table."""

    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    surname = Column(String(20))
    email = Column(String(50))
    wallet = Column(String(20))
    hashed_password = Column(String(50))
    date_joined = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=False)
