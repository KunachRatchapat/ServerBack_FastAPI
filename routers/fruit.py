from fastapi import APIRouter, HTTPException,Depends, Query, status
from typing import Annotated, Optional
from sqlmodel import select, Session
from db.models import fruit_model
from db.database import get_session
from depencies.dependencies import  get_current_admin_user
from db.models.user_model import Users

Fruit = fruit_model.Fruit

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]
AdminUserDep = Annotated[Users, Depends(get_current_admin_user)]

#--เพิ่มผลไม้ (เฉพาะแอดมินนะ)--
@router.post("/fruit",response_model=Fruit)
def create_fruit(fruit: Fruit, session:SessionDep, admin:AdminUserDep):
    try:    
        session.add(fruit)
        session.commit()
        session.refresh(fruit)
        print("Add Fruit Success",fruit.name)
        return fruit
    
    except Exception as e:
        print("Error Add Fruit !!", str(e))
        raise HTTPException(status_code=500, detail="Failed to Add Fruit")
    
    
#--โชว์ผลไม้ทั้งหมด--
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

#--เรียกดู ผลไม้ทีละตัว --    
@router.get("/fruit/{fruit_id}", response_model=Fruit)
def get_fruit_id(fruit_id:int, session:SessionDep):
    fruit = session.get(Fruit, fruit_id)
    if not fruit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fruit not Found !!")
    
    
    
#-- อัปเดตผลไม้ (สิทธิ์นี้ให้แอดมินงับ)--
@router.put("/fruit/{fruit_id}", response_model=Fruit)
def update_fruit(fruit_id:int, admin:AdminUserDep, fruit_update:Fruit, session:SessionDep):
    fruit = session.get(Fruit, fruit_id)
    if not fruit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fruit Not Found !!")
    
    update_fruit =  fruit_update.model_dump(exclude_unset=True)
    for key, value in update_fruit.items():
        setattr(fruit, key, value)
        
    session.add(fruit)
    session.commit()
    session.refresh(fruit)
    
    return fruit
       
    
#---Delete Fruit---
@router.delete("/fruit/{fruit_id}")
def delete_fruit(fruit_id:int, session:SessionDep, admin:AdminUserDep):
    fruit = session.get(Fruit, fruit_id)
    if not fruit:
        raise HTTPException(status_code=404,detail="Fruit not Found")
    session.delete(fruit)
    session.commit()
    return 
        
        
                              