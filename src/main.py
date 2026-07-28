from fastapi import FastAPI
from pydantic import BaseModel

from .routes.actor import router as actor_router
from .routes.customer import router as customer_router
from .routes.inventory import router as inventory_router
from .routes.rental import router as rental_router


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

app.include_router(actor_router)
app.include_router(customer_router)
app.include_router(inventory_router)
app.include_router(rental_router)


@app.get("/health")
def health_checkpoint():
    return "Working correctly"
