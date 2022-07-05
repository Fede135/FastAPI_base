from typing import Union

from fastapi import Depends, FastAPI, HTTPException

from fastapi_pagination import Page, add_pagination

from app.schemas.competition import Competition
from app.schemas.player import Player
import sql_app.crud.competition as crud_competition
import sql_app.crud.player as crud_player
from sql_app.database import SessionLocal
from app.utils.football_api_proxy import Proxy
from app.utils.utils import get_api_footbal_url


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/league/{league_code}/import", response_model=Competition)
def import_league(league_code: str, db: SessionLocal = Depends(get_db)):
    try:
        competition_with_teams = crud_competition.get_competition(db, league_code)

        if competition_with_teams is not None:
            return competition_with_teams

        competition_url = get_api_footbal_url() + 'competitions/{}/teams'.format(league_code)

        proxy = Proxy()
        response = proxy.get(competition_url)

        if response.status_code < 200 or response.status_code > 299:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()
            )

        response_json = response.json()
        competition = response_json['competition']
        teams = response_json['teams']

        competition_with_teams = crud_competition.create_competition_with_teams_and_players(
            db,
            proxy,
            competition,
            teams
        )
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return competition_with_teams


@app.get("/league/{league_code}/players", response_model=Page[Player])
def get_players_from_league(league_code: str, team_name: Union[str, None] = None, db: SessionLocal = Depends(get_db)):
    try:
        competition_with_teams = crud_competition.get_competition(db, league_code)

        if competition_with_teams is None:
            raise HTTPException(
                status_code=404,
                detail="League %s not found" % league_code
            )

        return crud_player.get_players_from_teams(db, competition_with_teams.teams, team_name)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


add_pagination(app)

