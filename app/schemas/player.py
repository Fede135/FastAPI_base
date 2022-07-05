from typing import Optional, Union
from datetime import date

from pydantic import BaseModel


class Player(BaseModel):
    name: Union[str, None] = None
    position: Union[str, None] = None
    dateOfBirth: Optional[date] = None
    countryOfBirth: Union[str, None] = None
    nationality: Union[str, None] = None

    class Config:
        orm_mode = True
