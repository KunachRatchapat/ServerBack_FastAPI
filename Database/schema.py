from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime 

#Table User
class Users (SQLModel , table = True):
    id : int = Field(default =None, primary_key=True)
    email : str = Field()
    password : str = Field()
    name : str = Field(index = True)
    surname : str = Field()
    createat : datetime = Field()
    deleteat : datetime = Field()
    updateat : datetime = Field()
    identification : str = Field()
    
#Table Vegetable
class Vegetable (SQLModel , table=True):
    id : int = Field(default= None, primary_key=True)
    name : str = Field(index = True)
    description : str = Field()
    picture : str =  Field(index = True)
    createat : datetime = Field(default_factory=datetime.now)
    deleteat: datetime = Field(default_factory=datetime.now)
    updateat: datetime = Field(default_factory=datetime.now)
    
#Table Favorite
class Favorite (SQLModel , table = True):
    id : int = Field(default = None , primary_key = True)
    user : Users
    vegetables : Vegetable
    createat : datetime = Field(defalt_factory =datetime.now)
    deleteat : datetime = Field(default_factory=datetime.now)
    updateat : datetime = Field(default_factory=datetime.now)
    
    
    
    
