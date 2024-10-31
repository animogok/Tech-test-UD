import datetime
import http.client
import json
from typing import List, Optional, Union
from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from pydantic import BaseModel, EmailStr

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Odd(BaseModel):
    value: str
    odd: str


class SportEvent(BaseModel):
    fixture_id: int
    league_id: int
    season: str
    team_home: str
    team_away: str
    goals_home: int
    goals_away: int
    last_updated: str

    class Config:
        arbitrary_types_allowed = True  # Permitir tipos arbitrarios


class SportEventOdds(SportEvent):
    odds: List[Odd]

    class Config:
        arbitrary_types_allowed = True


class SportBet(BaseModel):
    fixture_id: int
    bet_amount: float = 0
    bet_goals: str
    odd_value: float = 0
    date: str
    user_email: EmailStr


class SportEventUser(SportEvent):
    user_email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    """
    Represents the structure of a token response.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token (usually "bearer").
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Represents the structure of token data extracted from the JWT.

    Attributes:
        email (EmailStr): The email of the user associated with the token.
    """

    email: EmailStr


class ErrorResponse(BaseModel):
    detail: str


def get_sports_API():

    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")
    headers = {
        "x-rapidapi-key": "1d2e07eb18mshfc359e8e8dd7ce3p157b30jsn1f9d45479876",
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    }
    conn.request("GET", "/v3/odds/live", headers=headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def parse_event_data(
    data: str, fixture_id: Optional[int] = None
) -> Union[List[SportEvent], ErrorResponse]:
    data_json = json.loads(data)
    event_data = data_json["response"]
    df = pd.json_normalize(event_data)

    if fixture_id is not None:
        df = df[df["fixture.id"] == fixture_id]
        if df.empty:
            return ErrorResponse(detail="There is no odds available for this fixture")

        event = df.iloc[0].to_dict()

        # Filtrar odds donde odds.name sea igual a "Final Score"
        odds_data = event.get("odds", [])
        final_score_odds = [odd for odd in odds_data if odd["id"] == 23]

        if final_score_odds:
            odds_list = [
                Odd(value=odd["value"], odd=odd["odd"])
                for odd in final_score_odds[0]["values"]
            ]

            sport_event = SportEventOdds(
                fixture_id=event["fixture.id"],
                league_id=event["league.id"],
                season=str(event["league.season"]),
                team_home=str(event["teams.home.id"]),
                team_away=str(event["teams.away.id"]),
                goals_home=event["teams.home.goals"],
                goals_away=event["teams.away.goals"],
                last_updated=str(
                    datetime.datetime.strptime(event["update"], "%Y-%m-%dT%H:%M:%S%z")
                ),
                odds=odds_list,
            )
            return sport_event
        else:
            return ErrorResponse(detail="There is no odds available for this fixture")

    events_dict = df.to_dict(orient="records")
    events = [
        SportEvent(
            fixture_id=event["fixture.id"],
            league_id=event["league.id"],
            season=str(event["league.season"]),
            team_home=str(event["teams.home.id"]),
            team_away=str(event["teams.away.id"]),
            goals_home=event["teams.home.goals"],
            goals_away=event["teams.away.goals"],
            last_updated=str(
                datetime.datetime.strptime(event["update"], "%Y-%m-%dT%H:%M:%S%z")
            ),
        )
        for event in events_dict
    ]
    return events


# ==================================AUTH JWT====================================================#


async def very_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    validate_url = ".../validate-token/"
    headers = {"Authorization": token}

    response = request.client.get(validate_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
