from typing import Union
from fastapi import FastAPI , Request ,APIRouter
   
router = APIRouter()

@router.post("/vegetable")
async def add_vegetable():
        return {"Hello Addvet"}
    
    
@router.get("/vegetable")
async def read_vegetables():
    return {"Show Vet"}

@router.get("vegetable/{vet_id}")
async def read_vegetable():
    return {"Show bobo"}
    

