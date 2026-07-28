
from ..db.engine import get_db
from typing import Annotated
from fastapi import Depends, Query
from ..models.actor import Actor, Film, FilmActor
from sqlalchemy.orm import Session
from sqlalchemy import select


def get_actors_paginated(
    db: Session,
    last_id: int | None = None,
    page_limit: Annotated[int, Query(ge=1, le=100)] = 10
) -> list[Actor]:

    stmtn = select(Actor)
    if last_id is not None:
        stmtn = stmtn.where(Actor.actor_id < last_id)
    
    stmtn = stmtn.order_by(Actor.actor_id.desc()).limit(page_limit)

    actors = db.scalars(stmtn).all()
    return {
        "items": actors,
        "next_cursor": actors[-1].actor_id if actors else None
    }

def get_movies_by_actor(
        db: Session,
        actor_full_name: str,
        sort_desc: bool = True
):
    first_name, last_name = actor_full_name.split(" ")
    sorting = Film.release_year.desc() if sort_desc else Film.release_year.asc()
    stmtn = select(
            Film.title, Film.release_year, Film.rental_rate, Film.rating
        ).join(
            FilmActor, Film.film_id == FilmActor.film_id
        ).join(
            Actor, Actor.actor_id == FilmActor.actor_id
        ).where(
            Actor.first_name == first_name and Actor.last_name == last_name
        ).order_by(sorting)

    return db.execute(stmtn).mappings().all()