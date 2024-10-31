from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship
from SQL.engine import Base


class Event(Base):
    __tablename__ = "sport_event"
    id = Column(Integer, primary_key=True)
    fixture_id = Column(Integer)
    bet_amount = Column(Float)
    bet_goals = Column(String)
    odd_value = Column(String)
    date = Column(DateTime)
    user_email = Column(String, ForeignKey("User.email", ondelete="CASCADE"))
    user = relationship("UserDb", back_populates="bets")
