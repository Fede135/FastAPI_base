from sqlalchemy.orm import Session

from sql_app.models import Team


def get_count_teams(db: Session):
    return db.query(Team).count()
