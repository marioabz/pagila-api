from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class CustomerModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    store_id: int
    first_name: str
    last_name: str
    email: str | None
    address_id: int
    activebool: bool
    create_date: date
    last_update: datetime
    active: int
