import re
from typing import Optional
from sqlalchemy.orm import Session
from .models import Event


def create_bet(
    db: Session,
    fixture_id: int,
    odd_value: float,
    date: str,
    bet_amount: float,
    bet_goals: str,
    user_email: str,
):
    event_db = Event(
        fixture_id=fixture_id,
        bet_amount=bet_amount,
        bet_goals=bet_goals,
        odd_value=odd_value,
        date=date,
        user_email=user_email,
    )
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db
