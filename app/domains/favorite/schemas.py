from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FavoriteToggle(BaseModel):
    vegetable_id: Optional[int] = None
    fruit_id: Optional[int] = None


class FavoriteItemResponse(BaseModel):
    id: int
    user_id: int
    type: str
    item_id: int
    item_name: str
    item_description: Optional[str] = None
    item_image_url: Optional[str] = None
    createat: datetime
