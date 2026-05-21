from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FruitCreate(BaseModel):
    name: str
    picture: str
    description: Optional[str] = None


class FruitUpdate(BaseModel):
    name: Optional[str] = None
    picture: Optional[str] = None
    description: Optional[str] = None


class FruitResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    picture: str
    description: Optional[str] = None
    createat: datetime
