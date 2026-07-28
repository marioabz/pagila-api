from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InventoryModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    inventory_id: int
    film_id: int
    store_id: int
    last_update: datetime
