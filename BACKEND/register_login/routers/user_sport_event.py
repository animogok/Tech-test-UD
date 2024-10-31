from datetime import datetime
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from models.sport_event import (
    Bet,
    SportEvent,
    SportEventBets,
    UserSportEvent,
    calculate_odd,
)
from SQL.engine import SessionLocal
from SQL.crud import (
    get_all_sport_events,
    get_sport_event,
    get_sport_event_bets,
    post_bet,
    post_sport_event,
    update_sport_event,
    update_user,
)


from models.user import User, active_user

sport_router = APIRouter()

# ============================= GET =====================================================#


@sport_router.get("/sport-events/", response_model=List[UserSportEvent])
def read_all_sport_events():
    events = get_all_sport_events()
    return [UserSportEvent.from_orm(event) for event in events]


@sport_router.get("/sport-events/bets", response_model=SportEventBets)
def real_sport_event_bets(
    event_id: int, current_user: Annotated[User, Depends(active_user)]
):
    bets = get_sport_event_bets(event_id=event_id)
    event = get_sport_event(db=SessionLocal(), event_id=event_id)

    # Verificar la propiedad del evento
    if current_user.email != event.user_email:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this event"
        )

    # Filtrar solo los campos relevantes para cada `Bet` en bets
    bets_list = [
        Bet(
            team_home_score_pred=bet.team_home_score_pred,
            team_away_score_pred=bet.team_away_score_pred,
            cash=bet.cash,
            odd=bet.odd,
            user_email=bet.user_email,
            event_id=bet.sport_event_id,
        )
        for bet in bets
    ]

    # Crear el objeto `SportEventBets` y convertir `event_final_date` a string
    sport_event_with_bets = SportEventBets(
        id=event.id,
        event_name=event.event_name,
        event_final_date=event.event_final_date.strftime("%Y/%m/%d %H:%M"),
        event_type=event.event_type,
        team_home=event.team_home,
        team_away=event.team_away,
        bets=bets_list,
    )

    return sport_event_with_bets


# =========================== POST ========================================================#


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
    post_sport_event(event_info=list_data, user=current_user.email)


@sport_router.post("/user-new-bet/")
def post_sport_bet(
    event_id: int,
    score1: int,
    score2: int,
    cash: float,
    current_user: Annotated[User, Depends(active_user)],
):
    if score1 < 0 or score2 < 0:
        raise HTTPException(
            status_code=400, detail="The score prediction can't be negative number"
        )

    if get_sport_event(db=SessionLocal(), event_id=event_id):

        if cash < float(current_user.wallet):
            update_user(wallet=(-1 * cash), current_user=current_user)
            print("hola")
            return post_bet(
                event_id=event_id,
                user_email=current_user.email,
                pred1=score1,
                pred2=score2,
                cash=cash,
            )
        else:
            raise HTTPException(
                status_code=400, detail="Not enough money in the wallet"
            )
    else:
        return HTTPException(status_code=400, detail="Sport event doesn't found")


# =================================================================================== #


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
