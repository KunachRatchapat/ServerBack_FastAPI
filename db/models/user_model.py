from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .favorite_model import Favorite

# ---Table User---
class Users(SQLModel, table=True): # เปลี่ยนชื่อคลาสเป็น Users ให้ตรงกับที่คุณใช้ใน Favorite model
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field()
    password: str = Field()
    username: str = Field(index=True)
    surname: str = Field()
    role: str = Field(default="user")

    createat: datetime = Field(default_factory=datetime.now)
    deleteat: Optional[datetime] = Field(default=None, nullable=True)
    updateat: Optional[datetime] = Field(default=None, nullable=True)

    # Relationship 1 to M

    favorites: List["Favorite"] = Relationship(back_populates="user")