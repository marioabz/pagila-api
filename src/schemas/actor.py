
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ActorModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    actor_id: int = Field()
    first_name: str = Field()
    last_name: str = Field()
    last_update: datetime = Field()


class FilmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    film_id: int = Field()
    title: str = Field()
    description: str = Field()
    release_year: int = Field()
    rental_rate: float = Field()
    rating: int = Field()


class FilmSummaryModel(BaseModel):
    title: str
    release_year: int | None
    rental_rate: float
    rating: str | None

