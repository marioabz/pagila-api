from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RentalModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rental_id: int
    rental_date: datetime
    inventory_id: int
    customer_id: int
    return_date: datetime | None
    staff_id: int
    last_update: datetime
