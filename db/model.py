from typing import Optional , List
from sqlmodel import Field, SQLModel , Relationship
from datetime import datetime 
 
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
    
#---Table User---
class Users(SQLModel , table = True):
    id : Optional[int] = Field(default =None, primary_key=True)
    email : str = Field()
    password : str = Field()
    name : str = Field(index = True)
    surname : str = Field()
    identification : str = Field()
    createat : datetime = Field(default_factory=datetime.now)
    deleteat: Optional[datetime] = Field(default=None, nullable=True)
    updateat : Optional[datetime] = Field(default=None, nullable=True)

    #Relationship 1 to M
    favorites: List[Favorite] = Relationship(back_populates="user")
    
    
#---Table Vegetable---
class Vegetable(SQLModel , table=True):
    id : Optional[int] = Field(default= None, primary_key=True)
    name : str = Field(index = True)
    description : str = Field()
    picture : str 
    createat : datetime = Field(default_factory=datetime.now)
    deleteat: Optional[datetime] = Field(default=None, nullable=True)
    updateat: Optional[datetime] = Field(default=None, nullable=True)
    
    #Relationship 1 to M
    favorites : List[Favorite] = Relationship(back_populates="vegetable")
    
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
    
    
    
    
