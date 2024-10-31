from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException
import models.SportEventModels as sem
from SQL.crud import create_bet
from SQL.engine import SessionLocal


sport_router = APIRouter()


@sport_router.get("/sport-events/", response_model=List[sem.SportEvent])
def get_sport_events():
    data = sem.get_sports_API()
    events = sem.parse_event_data(data)
    return events
    """if user:
        data = sem.get_sports_API()
        events = sem.parse_event_data(data)
        return events
    else:
        return {"detail": "Something went wrong"}"""


def create_new_bet(fixture_id: int):
    try:
        data = sem.get_sports_API()
        events = sem.parse_event_data(data=data, fixture_id=fixture_id)

        # Verificar si la respuesta es un ErrorResponse
        if isinstance(events, sem.ErrorResponse):
            raise HTTPException(status_code=404, detail=events.detail)

        return events

    except Exception as e:
        raise HTTPException(status_code=404, detail="There is no odd for this fixture")


@sport_router.post("/football-event/new", response_model=sem.SportBet)
async def create_football_event_bet(fixture_id: int, goals_home: int, goals_away: int):
    db = SessionLocal()
    goals = "-".join([str(goals_home), str(goals_away)])
    odd_team = dict(create_new_bet(fixture_id=fixture_id))
    for item in odd_team.get("odds"):
        if dict(item).get("values") == goals:
            create_bet(
                db=db,
                fixture_id=fixture_id,
                odd_value=dict(item).get("odd"),
                date=odd_team.get("last_updated"),
                bet_amount=0,
                bet_goals=goals,
                user_email="asd@exama.sd",
            )

    return sem.SportBet(
        fixture_id=fixture_id,
        odd_value=dict(item).get("odd"),
        date=odd_team.get("last_updated"),
        bet_amount=0,
        bet_goals=goals,
        user_email="asd@exama.sd",
    )
