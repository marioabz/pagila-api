
from typing import Annotated

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from .schemas.actor import ActorModel, FilmSummaryModel
from .db.engine import get_db
from .service.actor import get_actors_paginated, get_movies_by_actor


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    active: bool


app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello world from FastAPI"}


@app.get("/list_actors")
def get_actors(
    db: Annotated[Session, Depends(get_db)],
    last_id: int | None = None,
    page_limit: int | None = 10,
):
    actors = get_actors_paginated(db, last_id=last_id, page_limit=page_limit)
    return [ActorModel.model_validate(result.__dict__) for result in actors["items"]]


@app.get("/get_movies_by_actor_full_name")
def get_films_by_actor_full_name(
    db: Annotated[Session, Depends(get_db)],
    actor_full_name: str,
    sort_desc: bool = True
):
    results = get_movies_by_actor(db, actor_full_name, sort_desc)
    return [FilmSummaryModel.model_validate(result) for result in results]


@app.get("/health")
def health_checkpoint():
    return "Working correctly"
