from fastapi import FastAPI
from pydantic import BaseModel
from .routes.actor import router


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

app.include_router(router)


@app.get("/health")
def health_checkpoint():
    return "Working correctly"
