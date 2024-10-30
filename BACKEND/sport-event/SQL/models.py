import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float
from SQL.engine import Base


class Event(Base):
    __tablename__ = "sport event"
