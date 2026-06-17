from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class FavoriteToggle(BaseModel):
    vegetable_id: Optional[int] = None
    fruit_id: Optional[int] = None

    @model_validator(mode="after")
    def check_exactly_one_target(self):
        has_fruit = self.fruit_id is not None
        has_vegetable = self.vegetable_id is not None
        if has_fruit == has_vegetable:
            raise ValueError("Exactly one of fruit_id or vegetable_id must be provided")
        return self


class FavoriteItemResponse(BaseModel):
    id: int
    user_id: int
    type: str
    item_id: int
    item_name: str
    item_description: Optional[str] = None
    item_image_url: Optional[str] = None
    createat: datetime
