from os import environ

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import models, schemas, crud

from .database import SessionLocal, engine

from .queue import send_message_to_queue

SERVER_NAME = environ.get('NAME')

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/links", response_model=schemas.Link)
async def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    db_link = crud.create_link(db, link)
    send_message_to_queue(db_link)
    return db_link


@app.get("/links/{link_id}", response_model=schemas.Link)
async def get_link(link_id: int, db: Session = Depends(get_db)):
    db_link = crud.get_link(db, link_id=link_id)
    if db_link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return db_link


@app.put("/links/{link_id}", response_model=schemas.Link)
async def update_link(link_id: int, link: schemas.LinkUpdate, db: Session = Depends(get_db)):
    db_link = crud.update_link(db, link_id, link_update=link)
    if db_link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return db_link


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Server-Name"] = SERVER_NAME
    return response
