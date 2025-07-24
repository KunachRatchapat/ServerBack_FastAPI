from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import select, Session
from typing import Annotated
from db.database import get_session
from db.models.fruit_model import Fruit
from db.models.vegetable_model import Vegetable

router = APIRouter()
SessionDep = Annotated[Session,Depends(get_session)]

@router.get("/search",response_model=list[dict])
def search_Veggie(
    session : SessionDep,
    keyword : str = Query(... , description="ชื่อผักหรือผลไม้ที่ต้องการค้นหา")   
):
    try:
        fruit_result = session.exec(
            select(Fruit).where(Fruit.name.contains(keyword))
        ).all()
        
        veg_result = session.exec(
            select(Vegetable).where(Vegetable.name.contains(keyword))
        ).all()
        
        results = [{"name": f.name} for f in fruit_result] + \
                  [{"name :" v.name} for v in  veg_result]
        
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Search Failed")
    