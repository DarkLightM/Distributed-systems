from typing import Optional

from sqlalchemy.orm import Session

from . import models, schemas


def get_link(db: Session, link_id: int) -> Optional[models.Link]:
    return db.query(models.Link).filter(models.Link.id == link_id).first()


def create_link(db: Session, link: schemas.LinkCreate) -> models.Link:
    db_link = models.Link(url=link.url)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link
