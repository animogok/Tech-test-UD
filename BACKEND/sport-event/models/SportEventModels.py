import datetime
import http.client
import json
from pydantic import BaseModel


class Event:
    def __init__(
        self,
        fixture_id: int,
        season: str,
        team_home: str,
        team_away: str,
        goals_home: int,
        goals_away: int,
        last_updated: datetime,
    ):
        self.fixture_id = fixture_id
        self.season = season
        self.team_home = team_home
        self.team_away = team_away
        self.goals_home = goals_home
        self.goals_away = goals_away
        self.last_updated = last_updated


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


def parse_event_data(data):
    data_json = json.loads(data)
    event_data = data_json["response"][0]

    fixture_id = event_data["fixture"]["id"]
    season = str(event_data["league"]["season"])
    team_home = str(event_data["teams"]["home"]["id"])
    team_away = str(event_data["teams"]["away"]["id"])
    goals_home = event_data["teams"]["home"]["goals"]
    goals_away = event_data["teams"]["away"]["goals"]
    last_updated = datetime.datetime.strptime(
        event_data["update"], "%Y-%m-%dT%H:%M:%S%z"
    )

    event = Event(
        fixture_id=fixture_id,
        season=season,
        team_home=team_home,
        team_away=team_away,
        goals_home=goals_home,
        goals_away=goals_away,
        last_updated=last_updated,
    )
    return event


data = get_sports_API()
event = parse_event_data(data=data)
print(event)
