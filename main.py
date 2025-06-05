from typing import Union

#Database Import
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker

#library Fast
from fastapi import FastAPI , Request 
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

#create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False}
)

#Create Base class For model use ORM
Base = declarative_base()

# Create session Connect DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#router
app = FastAPI()

#define for variable
class Item(BaseModel):
    name: str
    description:str
    price: float
    
    

@app.get("/items/{item_id}")
def read_item(item_id: int,q :Union[str,None] = None): #use Union for have query or No query string
    return {"item_id": item_id,"q":q}


@app.post("/items")
def create_item(item: Item):
    print(item.name , item.price,item.description)
    return { "request body": item }  #send Frontend JSON

@app.put("items/{item_id}")
def edit_item(item_id:int ,item:Item):
    return {"id":item_id,"body":item}


@app.delete("items/{item_id}")
def delete_item(item_id:int ):
   return {"message":f"Item {item_id} deleteds" } #format string message