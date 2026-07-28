from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..db.engine import get_db
from ..schemas.customer import CustomerModel

router = APIRouter(prefix="/customers", tags=["customers"])

DatabaseSession = Annotated[Session, Depends(get_db)]
PageLimit = Annotated[int, Query(ge=1, le=100)]


@router.get("", response_model=list[CustomerModel])
def list_customers(
    db: DatabaseSession,
    last_id: int | None = None,
    page_limit: PageLimit = 10,
):
    # TODO: Add the customer listing service call.
    return []


@router.get("/{customer_id}", response_model=CustomerModel)
def get_customer(customer_id: int, db: DatabaseSession):
    # TODO: Add the customer lookup service call.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Customer lookup is not implemented yet",
    )
