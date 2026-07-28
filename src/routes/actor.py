from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db.engine import get_db
from ..schemas.actor import ActorModel, FilmSummaryModel
from ..service.actor import get_actors_paginated, get_movies_by_actor


router = APIRouter(
    prefix="/actors",
    tags=["actors"]
)

@router.get("", response_model=list[ActorModel])
def list_actors(
    db: Annotated[Session, Depends(get_db)],
    last_id: int | None = None,
    page_limit: int | None = 10,
):
    actors = get_actors_paginated(db, last_id=last_id, page_limit=page_limit)
    return [ActorModel.model_validate(result.__dict__) for result in actors["items"]]

@router.get("/by-name/{actor_full_name}/films", response_model=list[FilmSummaryModel])
def get_films_by_actor_full_name(
    db: Annotated[Session, Depends(get_db)],
    actor_full_name: str,
    sort_desc: bool = True
):
    results = get_movies_by_actor(db, actor_full_name, sort_desc)
    return [FilmSummaryModel.model_validate(result) for result in results]
