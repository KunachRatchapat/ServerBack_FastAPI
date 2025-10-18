from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Annotated , Optional
from sqlmodel import select, Session
from db.models import vegetable_model 
from db.database import get_session
from db.models.user_model import Users
from depencies.dependencies import get_current_admin_user
from schema.vegetable_schema import VegetableUpdate

Vegetable =  vegetable_model.Vegetable

router = APIRouter() 

SessionDep = Annotated[Session, Depends(get_session)]
AdminUserDep = Annotated[Users, Depends(get_current_admin_user)]


#--เพิ่มผัก-- 
@router.post("/vegetable", response_model=Vegetable)
def create_vegetable(vegetable: Vegetable, session: SessionDep, admin:AdminUserDep):
    try:
        session.add(vegetable)
        session.commit()
        session.refresh(vegetable)
        print("Add Vegetable Success",vegetable.name)
        return vegetable
        
    except Exception as e :
        print("Error Add Vegetable !!",str(e))
        raise HTTPException(status_code=500, detail="Failed to add vegetable")
    
#--โชว์ผักทั้งหมด-- 
@router.get("/vegetables", response_model=list[Vegetable])
def read_vegetables(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    try:  
        vegetables = session.exec(select(Vegetable).offset(offset).limit(limit)).all()
        print("Show Vegetables")
        return vegetables
    
    except Exception as e:
      print("Error Show Vegetables")
      raise HTTPException(status_code=500)  
  
  
#--เรียกดูผักทีละตัว--
@router.get("/vegetable/{vegetable_id}", response_model=Vegetable)
def get_vet_id(vegetable_id:int, session:SessionDep):
    vegetable = session.get(Vegetable,vegetable_id)
    if not vegetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vegetable Not found")
    
#-- อัปเดตผัก (สิทธิ์นี้ให้แอดมินงับ)--
@router.put("/vegetable/{vegetable_id}", response_model=Vegetable)
def update_vegetable(vegetable_id:int, admin:AdminUserDep, vegetable_update:Vegetable, session:SessionDep):
    vegetable = session.get(Vegetable, vegetable_id)
    if not vegetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fruit Not Found !!")
    
    update_fruit =  vegetable_update.model_dump(exclude_unset=True)
    
    for key, value in update_fruit.items():
        setattr(vegetable, key, value)
        
    session.add(vegetable)
    session.commit()
    session.refresh(vegetable)
    
    return vegetable
    
        
#--ลบผัก--
@router.delete("/vegetable/{vegetable_id}")
def delete_vegetable(vegetable_id: int, session: SessionDep):
    vegetable = session.get(Vegetable, vegetable_id)
    if not vegetable:
        raise HTTPException(status_code=404, detail="Vegetable not found")
    session.delete(vegetable)
    session.commit()
    return 
