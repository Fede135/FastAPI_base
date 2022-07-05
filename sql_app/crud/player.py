from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from sql_app.models import Player, Team


def get_players_from_teams(db: Session, teams: List[Team], team_name: str = None) -> List[Player]:
    team_ids = [team.id for team in teams]
    filters = [Team.id.in_(team_ids)]

    if team_name:
        # Giving the possibility to filter by name or shortName
        filters.append(or_(Team.shortName == team_name, Team.name == team_name))

    return paginate(db.query(Player).join(Team).filter(*filters))


def get_count_players(db: Session):
    return db.query(Player).count()
