from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:  # <<< เพิ่ม if TYPE_CHECKING
    from .favorite_model import Favorite  # <<< ย้ายมาไว้ใน if TYPE_CHECKING


# ---Table Vegetable---
class Vegetable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    picture: str
    description: Optional[str] = Field(default=None)
    createat: datetime = Field(default_factory=datetime.now)
    deleteat: Optional[datetime] = Field(default=None, nullable=True)
    updateat: Optional[datetime] = Field(default=None, nullable=True)

    # Relationship 1 to M
    favorites: List["Favorite"] = Relationship(back_populates="vegetable")
