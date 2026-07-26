from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db.engine import get_db
from .models.actor import Actor


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


class ActorModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    actor_id: int = Field()
    first_name: str = Field()
    last_name: str = Field()
    last_update: datetime = Field()


app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello world from FastAPI"}


@app.get("/list_actors")
def get_actors(db: Annotated[Session, Depends(get_db)]):

    statement = select(Actor).where(Actor.actor_id <= 10)
    results = db.execute(statement).all()
    return [ActorModel.model_validate(result[0].__dict__) for result in results]


@app.get("/health")
def health_checkpoint():
    return "Working correctly"
