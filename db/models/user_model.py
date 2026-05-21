from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .favorite_model import Favorite

# ---Table User---
class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field()
    password: str = Field()
    username: str = Field(index=True)
    surname: str = Field()
    role: str = Field(default="user")

    is_verified: bool = Field(default=False)
    verify_token: Optional[str] = Field(default=None, nullable=True)
    reset_token: Optional[str] = Field(default=None, nullable=True)
    reset_token_expires: Optional[datetime] = Field(default=None, nullable=True)

    createat: datetime = Field(default_factory=datetime.now)
    deleteat: Optional[datetime] = Field(default=None, nullable=True)
    updateat: Optional[datetime] = Field(default=None, nullable=True)

    favorites: List["Favorite"] = Relationship(back_populates="user")