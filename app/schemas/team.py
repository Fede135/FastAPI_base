from typing import Union

from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str


class Team(TeamBase):
    tla: Union[str, None] = None
    shortName: Union[str, None] = None
    email: Union[str, None] = None
    areaName: Union[str, None] = None

    class Config:
        orm_mode = True
