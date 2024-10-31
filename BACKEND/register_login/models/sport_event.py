from re import T
from typing import Annotated, List
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr


class Bet(BaseModel):
    team_home_score_pred: int
    team_away_score_pred: int
    cash: float
    odd: float
    user_email: EmailStr
    event_id: int

    class Config:
        orm_mode = True


# =================================== SPOR EVENTS CLASSES ====================#


class SportEvent(BaseModel):
    id: int
    event_name: str
    event_final_date: str
    event_type: str
    team_home: str
    team_away: str


class UserSportEvent(SportEvent):
    user_email: EmailStr
    event_status: bool

    class Config:
        orm_mode = True


class SportEventBets(SportEvent):
    bets: List[Bet]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            event_name=obj.event_name,
            event_final_date=obj.event_final_date.strftime("%Y/%m/%d/%H/%M"),
            event_type=obj.event_type,
            team_home=obj.team_home,
            team_away=obj.team_away,
            bets=[
                Bet.from_orm(bet) for bet in obj.bets
            ],  # Convertir bets a instancias de Bet
        )


# ============================= FUNCTIONS RELATED TO THIS CLASSES =======================#


def calculate_odd(home_team_score: int, away_team_score: int) -> float:
    difference = home_team_score - away_team_score
    if difference > 0:

        odd = 1 + (0.1 * difference)
    elif difference < 0:

        odd = 1 + (0.1 * abs(difference))
    else:

        odd = 1.0
    return float(odd)
