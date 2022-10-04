import datetime

from pydantic import BaseModel


class LinkBase(BaseModel):
    url: str


class LinkCreate(LinkBase):
    pass


class Link(LinkBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
