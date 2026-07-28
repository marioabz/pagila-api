from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..db.engine import get_db
from ..schemas.rental import RentalModel

router = APIRouter(prefix="/rentals", tags=["rentals"])

DatabaseSession = Annotated[Session, Depends(get_db)]
PageLimit = Annotated[int, Query(ge=1, le=100)]


@router.get("", response_model=list[RentalModel])
def list_rentals(
    db: DatabaseSession,
    last_id: int | None = None,
    page_limit: PageLimit = 10,
):
    # TODO: Add the rental listing service call.
    return []


@router.get("/{rental_id}", response_model=RentalModel)
def get_rental(rental_id: int, db: DatabaseSession):
    # TODO: Add the rental lookup service call.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Rental lookup is not implemented yet",
    )
