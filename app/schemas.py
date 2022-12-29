import datetime
from typing import Optional

from pydantic import BaseModel


class LinkCreate(BaseModel):
    url: str


class LinkUpdate(BaseModel):
    status: str


class Link(BaseModel):
    id: int
    url: str
    status: Optional[str]
    created_at: datetime.datetime

    class Config:
        orm_mode = True
