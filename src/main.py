from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select

from .db.engine import Session
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


class Item(BaseModel):
    name: str
    price: float
    has_discount: bool


@app.get("/")
def hello_world():
    return {"message": "Hello world from FastAPI"}


@app.get("/list_actors")
def get_actors():
    with Session() as sess:
        statement = select(Actor).where(Actor.actor_id <= 10)
        results = sess.execute(statement).all()
        print(results[0][0].__dict__)
    return [ActorModel.model_validate(result[0].__dict__) for result in results]


@app.get("/health")
def health_checkpoint():
    return "Working correctly"
