from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import Annotated, Optional, List
from sqlmodel import select, Session
from db.models import favorite_model, fruit_model, vegetable_model 
from db.database import get_session
from pydantic import BaseModel
from schema.favorite_schema import FavoriteCreate,FavoriteRespone,FavoriteItemRespone
from fastapi.responses import JSONResponse
from db.models.favorite_model import Favorite
from db.models.vegetable_model import Vegetable
from db.models.fruit_model import Fruit

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


#---Add Favorite---
@router.post("/favorite/toggle",response_model=FavoriteRespone)
def toggle_favorite(favorite_data: FavoriteCreate , session: SessionDep):
    try:
        #Check ว่าเคยกดไลค์ยัง
        query = select(Favorite).where(Favorite.users_id == favorite_data.user_id)
        
        #--Check Vegetable already--
        if favorite_data.vegetable_id:
            query = query.where(Favorite.vegetable_id == favorite_data.vegetable_id)
            
        #--Check Fruit already--    
        if favorite_data.fruit_id:
            query = query.where(Favorite.fruit_id == favorite_data.fruit_id)
            
        #--Press Toggle Button--
        toggle = session.exec(query).first()
        print(JSONResponse(content={"message": "Favorite"}))
        
        if toggle:
            session.delete(toggle)
            session.commit()
            return JSONResponse(content={"message": "Unfavorite Success"} , status_code=200)
        
        #--Step 1 Add New ToggleButton--    
        new_toggle = Favorite(
            users_id = favorite_data.user_id,
            vegetable_id = favorite_data.vegetable_id,
            fruit_id = favorite_data.fruit_id
        ) 
        #--Step 2 Save New ToggleButton--
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
    
    
#--Show Favorite Vegetable--
@router.get("/favorites",response_model=List[FavoriteItemRespone])
def get_favorites(user_id : int , session : SessionDep):
    try:
        #--Search Favorite in DB use UserID == User Input Accept Where---
        favorites = session.exec( 
                select (Favorite).where(Favorite.users_id == user_id)
            ).all() 
        
        #--loop Respone list in DB Vegatable Fruit---
        response = []
        
        for f in favorites: 
            #
           if f.vegetable_id:
               veg = session.get(Vegetable, f.vegetable_id)
               if veg: #กัน veg เป็น none
                    response.append(FavoriteItemRespone(
                        id = f.id,
                        user_id = f.users_id,
                        type ="vegetable",
                        item_id = veg.id,
                        item_name = veg.name,
                        item_description = veg.description,
                        item_image_url = veg.picture,
                        createat = f.createat  
               ))
        #--If it's a Fruit favorite
           elif f.fruit_id:
               fruit = session.get(Fruit , f.fruit_id)
               if fruit: #กัน fruit เป็น none
                        response.append(FavoriteItemRespone(
                        id = f.id,
                        user_id = f.users_id,
                        type = "fruit",
                        item_id = fruit.id,
                        item_name = fruit.name,
                        item_description = fruit.description,
                        item_image_url = fruit.picture,
                        createat = f.createat
                   
               ))

        return response
    
    except Exception as e:
        print("Error Get Favorites",str(e))
        raise HTTPException(status_code=500,detail="Can't Fetch Favorites")
            
        