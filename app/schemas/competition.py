from typing import List, Union

from pydantic import BaseModel

from app.schemas.team import Team


class Competition(BaseModel):
    id: int
    name: str
    code: str
    areaName: Union[str, None] = None
    teams: Union[List[Team], None] = None

    class Config:
        orm_mode = True
