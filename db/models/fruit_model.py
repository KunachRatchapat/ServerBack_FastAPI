from typing import Optional , List
from sqlmodel import Field, SQLModel , Relationship
from datetime import datetime 
from .favorite_model import Favorite

#--Table Fruit--
class Fruit(SQLModel , table =True):
    id : Optional[int] = Field(default=None , primary_key=True)
    name : str = Field(index= True)
    description : str = Field()
    picture : str
    createat : datetime = Field(default_factory=datetime.now)
    deleteat: Optional[datetime] = Field(default=None, nullable=True)
    updateat: Optional[datetime] = Field(default=None, nullable=True)
    
    #Relationship 1 to M
    favorites : List[Favorite] = Relationship(back_populates="fruit")