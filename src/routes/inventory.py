from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..db.engine import get_db
from ..schemas.inventory import InventoryModel

router = APIRouter(prefix="/inventory", tags=["inventory"])

DatabaseSession = Annotated[Session, Depends(get_db)]
PageLimit = Annotated[int, Query(ge=1, le=100)]


@router.get("", response_model=list[InventoryModel])
def list_inventory(
    db: DatabaseSession,
    last_id: int | None = None,
    page_limit: PageLimit = 10,
):
    # TODO: Add the inventory listing service call.
    return []


@router.get("/{inventory_id}", response_model=InventoryModel)
def get_inventory_item(inventory_id: int, db: DatabaseSession):
    # TODO: Add the inventory lookup service call.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Inventory lookup is not implemented yet",
    )
