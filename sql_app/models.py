from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

competition_team = Table(
    'competition_team',
    Base.metadata,
    Column('team_id', ForeignKey('teams.id'), primary_key=True),
    Column('competition_id', ForeignKey('competitions.id'), primary_key=True)
)


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code = Column(String)
    areaName = Column(String)

    teams = relationship(
        'Team',
        secondary=competition_team,
        backref="competitions"
    )


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tla = Column(String, index=True)
    areaName = Column(String)
    shortName = Column(String)
    email = Column(String)

    players = relationship("Player", backref="player")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)
    position = Column(String)
    dateOfBirth = Column(Date)
    countryOfBirth = Column(String)
    nationality = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
