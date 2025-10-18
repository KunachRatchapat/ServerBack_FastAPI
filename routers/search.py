from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import select, Session, col
from typing import Annotated 
from db.database import get_session
from db.models.fruit_model import Fruit
from db.models.vegetable_model import Vegetable
from pydantic import BaseModel

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

class SearchResult(BaseModel):
    name: str


@router.get("/search", response_model=list[SearchResult])
def search_Veggie(
    session: SessionDep,
    keyword: str = Query(..., description="ชื่อผักหรือผลไม้ที่ต้องการค้นหา")
):
    try:
        fruit_result = session.exec(
            select(Fruit).where(col(Fruit.name).ilike(f"%{keyword}%"))
        ).all()
        
        veg_result = session.exec(
            select(Vegetable).where(col(Vegetable.name).ilike(f"%{keyword}%"))
        ).all()
        
        results = [{"name": f.name} for f in fruit_result] + \
                  [{"name": v.name} for v in veg_result]
        
        return results
    
    except Exception as e:
        print("Search Failed:", str(e))
        raise HTTPException(status_code=500, detail="Search Failed")
    

