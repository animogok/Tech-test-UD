from sqlalchemy import event
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from SQL.engine import Base, SessionLocal
import datetime


class UserDb(Base):
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

    # Columnas adicionales para el conteo de apuestas y eventos
    bets_count = Column(Integer, default=0)
    events_count = Column(Integer, default=0)

    events = relationship(
        "SportEvent", back_populates="user", cascade="all, delete-orphan"
    )

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
    bets_count = Column(Integer, default=0)

    user_email = Column(String(50), ForeignKey("User.email", ondelete="CASCADE"))

    user = relationship("UserDb", back_populates="events")

    bets = relationship("Bets", back_populates="event", cascade="all, delete-orphan")


class Bets(Base):
    __tablename__ = "Bet"
    id = Column(Integer, primary_key=True)
    odd = Column(Float)
    team_home_score_pred = Column(Integer)
    team_away_score_pred = Column(Integer)
    cash = Column(Float)
    earnings = Column(Float, default=0.0)
    win = Column(Boolean, default=False)

    user_email = Column(String(50), ForeignKey("User.email", ondelete="CASCADE"))

    sport_event_id = Column(Integer, ForeignKey("Sport_Event.id", ondelete="CASCADE"))

    user = relationship("UserDb", back_populates="bets")

    event = relationship("SportEvent", back_populates="bets")
