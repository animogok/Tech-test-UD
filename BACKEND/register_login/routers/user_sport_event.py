from datetime import datetime
from typing import Annotated, Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Path
from models.sport_event import Bets, SportEvent, calculate_odd
from SQL.crud import (
    get_all_sport_events,
    get_sport_event,
    post_bet,
    post_sport_event,
    update_sport_event,
)


from models.user import User, active_user

sport_router = APIRouter()


@sport_router.get("/sport-events/", response_model=list[SportEvent])
def read_all_sport_events():
    return get_all_sport_events()


@sport_router.post("/create-new-event/")
def create_event(
    event_name: str,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    event_type: str,
    team_home: str,
    team_away: str,
    current_user: Annotated[User, Depends(active_user)],
):
    date = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    print(date)
    list_data = [
        event_name,
        date.strftime(format="%Y/%m/%d/%H/%M"),
        event_type,
        team_home,
        team_away,
    ]
    post_sport_event(event_info=list_data, user_email=current_user.email)


@sport_router.post("/new-bet/", response_model=Bets)
def create_bet(data: Bets, current_user: Annotated[User, Depends(active_user)]):
    data_dict = dict(data)
    event = dict(get_sport_event(data_dict.get("event_id")))
    odd = calculate_odd(
        home_team_score=dict(event.get("team_home")).get("score"),
        away_team_score=dict(event.get("team_away")).get("score"),
    )
    if data_dict.get("cash") < current_user.wallet:
        return post_bet(bet_info=data_dict, odd=odd)

    raise HTTPException(status_code=400, detail="Not enough funds")


@sport_router.put("/sport-events/{event_id}", response_model=SportEvent)
def update_sport_event_endpoint(
    current_user: Annotated[User, Depends(active_user)],
    event_id: int,
    event_name: Optional[str] = None,
    event_type: Optional[str] = None,
    team_home: Optional[str] = None,
    team_away: Optional[str] = None,
):
    updated_event = update_sport_event(
        event_id=event_id,
        user_email=current_user.email,
        event_name=event_name,
        event_type=event_type,
        team_home=team_home,
        team_away=team_away,
    )
    if not updated_event:
        raise HTTPException(status_code=404, detail="SportEvent not found")
    return
