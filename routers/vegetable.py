from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Annotated
from sqlmodel import select, Session
from db.model import Vegetable
from db.database import get_session

router = APIRouter(prefix="/vegetables", tags=["Vegetables"]) 

SessionDep = Annotated[Session, Depends(get_session)]

#--Add Vegetable-- (For Dev)
@router.post("/vegetable", response_model=Vegetable)
def create_vegetable(vegetable: Vegetable, session: SessionDep):
    session.add(vegetable)
    session.commit()
    session.refresh(vegetable)
    return vegetable

#--Show All Vegetable-- (Home)
@router.get("/vegetables", response_model=list[Vegetable])
def read_vegetables(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    vegetables = session.exec(select(Vegetable).offset(offset).limit(limit)).all()
    return vegetables

#--Delete Vegetable--
@router.delete("/vegetable/{vegetable_id}")
def delete_vegetable(vegetable_id: int, session: SessionDep):
    vegetable = session.get(Vegetable, vegetable_id)
    if not vegetable:
        raise HTTPException(status_code=404, detail="Vegetable not found")
    session.delete(vegetable)
    session.commit()
    return {"Success": True}
