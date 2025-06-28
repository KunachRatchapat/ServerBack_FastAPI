from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Annotated
from sqlmodel import select, Session
from db.models import favorite_model , user_model
from db.database import get_session


Favorite = favorite_model.Favorite

router = APIRouter()

SessionDep = Annotated[Session , Depends(get_session)]

#-- Add Favorite--
@router.post("/favorite", response_model=Favorite)
def add_favorite(favorite:Favorite , session : SessionDep)
    try:
        session.add(favorite)
        session.commit()
        session.refresh(favorite)
        print("Add Favorite Successs")
        return favorite
        
    except Exception as e :
        print("Error Favorite !!",str(e))
        raise HTTPException(status_code=500, detail= "Failed to Add Favorite")
    
#--Show Favorite--
@router.get("/favorites", response_model=list[Favorite])       
def read_favorite()