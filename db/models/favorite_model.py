from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .vegetable_model import Vegetable
from .user_model import Users
from .fruit_model import Fruit


 
#---Table Favorite---
class Favorite(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    users_id: int = Field(foreign_key="users.id")         
    vegetable_id: int = Field(foreign_key="vegetable.id") 
    fruit_id: Optional[int] = Field(default=None, foreign_key="fruit.id") 
    createat: datetime = Field(default_factory=datetime.now)
    deleteat: Optional[datetime] = Field(default=None, nullable=True)
    updateat: Optional[datetime] = Field(default=None, nullable=True)
    
    #Relationship User to fav and Vegetable to fav
    user: Optional["Users"] = Relationship(back_populates="favorites")
    vegetable: Optional["Vegetable"] = Relationship(back_populates="favorites")
    fruit: Optional["Fruit"] = Relationship(back_populates="favorites")
    