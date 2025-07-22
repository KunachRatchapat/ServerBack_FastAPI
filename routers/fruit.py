from fastapi import APIRouter, HTTPException,Depends, Query
from typing import Annotated , Optional
from sqlmodel import select , Session
from db.models import fruit_model
from db.database import get_session

Fruit = fruit_model.Fruit

router = APIRouter()

SessionDep = Annotated[Session , Depends(get_session)]

#--Add Fruit--
@router.post("/fruit",response_model=Fruit)
def create_fruit(fruit: Fruit, session:SessionDep):
    try:
        session.add(fruit)
        session.commit()
        session.refresh(fruit)
        print("Add Fruit Success" ,fruit.name)
        return fruit
    
    except Exception as e:
        print("Error Add Fruit !!", str(e))
        raise HTTPException(status_code=500, detail="Failed to Add Fruit")
    
#--Show All Fruit--(Home)
@router.get("/fruits", response_model=list[Fruit])
def read_fruit(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    try:
        fruits = session.exec(select(Fruit).offset(offset).limit(limit)).all()
        print("Show Fruit")
        return fruits
    
    except Exception as e:
        print("Error Show Fruits")
        raise HTTPException(status_code=500)
        
        
                              