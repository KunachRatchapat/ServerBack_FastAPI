from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime 

#Table User
class Users (SQLModel , table = True):
    id : Optional[int] = Field(default =None, primary_key=True)
    email : str = Field()
    password : str = Field()
    name : str = Field(index = True)
    surname : str = Field()
    identification : str = Field()
    createat : datetime = Field(default_factory=datetime.now)
    deleteat : datetime = Field(default_factory=datetime.now)
    updateat : datetime = Field(default_factory=datetime.now)
    vegetable_id : int = Field(foreign_key="vegetable.id")  #relation with Vegetable
    favorite_id : int = Field(foreign_key="favorite.id")    #relation with Favorite
    
    
    
#Table Vegetable
class Vegetable (SQLModel , table=True):
    id : Optional[int] = Field(default= None, primary_key=True)
    name : str = Field(index = True)
    description : str = Field()
    picture : str =  Field(index = True)
    createat : datetime = Field(default_factory=datetime.now)
    deleteat: datetime = Field(default_factory=datetime.now)
    updateat: datetime = Field(default_factory=datetime.now)
    users_id : int = Field(foreign_key="user.id")   #relation with Users
    favorite_id : int = Field(foreign_key="favorite.id") #relation with Favorite
    
    
#Table Favorite
class Favorite (SQLModel , table = True):
    id : int = Field(default = None , primary_key = True)
    users_id :int = Field(foreign_key="user.id") #relation with Users
    vegetable_id : int = Field(foreign_key="vegetable.id") #relation with Vegetable
    createat : datetime = Field(default_factory=datetime.now)
    deleteat : datetime = Field(default_factory=datetime.now)
    updateat : datetime = Field(default_factory=datetime.now)
    
    
    
    
