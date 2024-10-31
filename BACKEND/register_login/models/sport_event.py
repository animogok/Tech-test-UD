import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator


class Bets(BaseModel):
    team_home_score_pred: int
    team_away_score_pred: int
    cash: float
    odd: float
    user_email: EmailStr
    event_id: int


class SportEvent(BaseModel):
    event_name: str
    event_final_date: str
    event_type: str
    team_home: str
    team_away: str


class SportEventBets(SportEvent):
    event_status: bool = False
    bets: List[Bets]


class UserSportEvent(SportEvent):
    user_email: EmailStr

    class Config:
        orm_mode = True


def calculate_odd(home_team_score: int, away_team_score: int) -> float:
    difference = home_team_score - away_team_score
    if difference > 0:

        odd = 1 + (0.1 * difference)
    elif difference < 0:

        odd = 1 + (0.1 * abs(difference))
    else:

        odd = 1.0
    return float(odd)
