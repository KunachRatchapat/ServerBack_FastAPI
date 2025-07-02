from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import Annotated , Optional , List 
from sqlmodel import select, Session
from db.models import favorite_model , user_model , fruit_model , vegetable_model 
from db.database import get_session
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import JSONResponse

#--Call Class Models--
Favorite = favorite_model.Favorite
Vegatable = vegetable_model.Vegetable
Fruit = fruit_model.Fruit

router = APIRouter()
SessionDep = Annotated[Session , Depends(get_session)]

#---Request Model---
class FavoriteCreate(BaseModel):
    user_id : int
    vegetable_id : Optional[int] = None
    fruit_id : Optional[int] = None

#---Respone Model---
class FavoriteRespone(BaseModel):
    id : int
    user_id : int
    vegetable_id : Optional[int] = None
    fruit_id : Optional[int] = None
    createat : datetime
    
#---Respone FavoriteItem---
class FavoriteItemRespone(BaseModel):
    id : int
    user_id : int
    type : str
    item_id : int
    item_name : str
    item_description : Optional[str] = None
    item_image_url : Optional[str] = None
    createat : datetime


#---Add Favorite---
@router.post("/favorite/toggle",response_model=FavoriteRespone)
def toggle_favorite(favorite_data: FavoriteCreate , session: SessionDep):
    try:
        #--Check ว่ามีรายการผักผลไม้นี้ไหม--
        query = select(Favorite).where(Favorite.users_id == favorite_data.user_id)
        
        #--Check Vegetablealready--
        if favorite_data.vegetable_id:
            query = query.where(Favorite.vegetable_id == favorite_data.vegetable_id)
            
        #--Check Fruitalready--    
        if favorite_data.fruit_id:
            query = query.where(Favorite.fruit_id == favorite_data.fruit_id)
            
        #--Press ToggleButton--
        toggle = session.exec(query).first()
        
        if toggle:
            session.delete(toggle)
            session.commit()
            return JSONResponse(content={"message": "Unfavorite Success"} , status_code=200)
        
        #--Step 1 AddNew ToggleButton--    
        new_toggle = Favorite(
            users_id = favorite_data.user_id,
            vegetable_id = favorite_data.vegetable_id,
            fruit_id = favorite_data.fruit_id
        ) 
        #--Step 2 Save NewToggleButton--
        session.add(new_toggle)
        session.commit()
        session.refresh(new_toggle) #save data
        
        return FavoriteRespone(
            id = new_toggle.id,
            user_id = new_toggle.users_id,
            vegetable_id = new_toggle.vegetable_id,
            fruit_id = new_toggle.fruit_id,
            createat = new_toggle.createat
        )
        
    except Exception as e:
        print(" Error Toggle Favorite",str(e))
        raise HTTPException(status_code=500 , detail="Server Error !!")