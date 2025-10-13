from typing import Optional , TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from pydantic import BaseModel


if TYPE_CHECKING: 
    from .user_model import Users
    from .vegetable_model import Vegetable
    from .fruit_model import Fruit
 
#---Table Favorite---
class Favorite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)       
    users_id: int = Field(foreign_key="users.id")  #เอา user.id จากตาราง Users       
    vegetable_id: Optional[int] = Field(default=None, foreign_key="vegetable.id") #เอา vegetable.id จากตาราง Vegetable   
    fruit_id: Optional[int] = Field(default=None, foreign_key="fruit.id")  #เอา fruit.id จากตาราง Fruit   
    createat: datetime = Field(default_factory=datetime.now)
    deleteat: Optional[datetime] = Field(default=None, nullable=True)
    updateat: Optional[datetime] = Field(default=None, nullable=True)
    
    #Relationship User to fav and Vegetable to fav
    user: Optional["Users"] = Relationship(back_populates="favorites")
    vegetable: Optional["Vegetable"] = Relationship(back_populates="favorites")
    fruit: Optional["Fruit"] = Relationship(back_populates="favorites")
    