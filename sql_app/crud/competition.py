from sqlalchemy.orm import Session

from app.utils.utils import load_players, Proxy
from sql_app.models import Competition, Team


def create_competition_with_teams_and_players(
        db: Session,
        proxy: Proxy,
        competition: dict,
        teams: dict
) -> Competition:
    db_competition = Competition(
        name=competition.get('name'),
        code=competition.get('code'),
        areaName=competition.get('area').get('name')
    )
    db_list = []

    for team in teams:

        db_team = Team(
            name=team.get('name'),
            tla=team.get('tla'),
            shortName=team.get('shortName'),
            areaName=team.get('area').get('name'),
            email=team.get('email'),
            players=load_players(team.get('id'), proxy)
        )

        db_list.append(db_team)

    db_competition.teams = db_list

    db_list.append(db_competition)

    db.add_all(db_list)
    db.commit()
    db.refresh(db_competition)
    db.refresh(db_team)
    return db_competition


def get_competition(db: Session, competition_code: str) -> Competition:
    return db.query(Competition).filter(Competition.code == competition_code).first()


def get_count_competitions(db: Session):
    return db.query(Competition).count()
