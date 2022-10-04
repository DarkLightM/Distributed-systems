import datetime

from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
