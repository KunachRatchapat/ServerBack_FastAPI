from pydantic import BaseModel
from datetime import datetime
from typing import Optional


#--- สำหรับสร้างผลไม้ ---
class FruitCreate(BaseModel):
    name : str
    picture : str 
    description: Optional[str]
    
    
#--  Respone อัปเดตผลไม้ --
class FruitUpdate(BaseModel):
    name: Optional[str] = None
    picture : Optional[str] = None
    description : Optional[str] = None
    
#-- Respone API --
class FruitRespone(BaseModel):
    id : int 
    name : str
    picture : str
    description : Optional[str]
    createat : datetime
    
    
class Config: #เพื่อให้สามารถอ่านข้อมูลจาก DB Model ได้โดยตรง
        from_attributes = True

    
    
    
    