from pydantic import BaseModel
from datetime import datetime
from typing import Optional


#--- สำหรับสร้างผัก ---
class VegetableCreate(BaseModel):
    name : str
    picture : str 
    description: Optional[str]
    
    
#--  Respone อัปเดตผัก --
class VegetableUpdate(BaseModel):
    name: Optional[str] = None
    picture : Optional[str] = None
    description : Optional[str] = None
    
#-- Respone API --
class VegetableRespone(BaseModel):
    id : int 
    name : str
    picture : str
    description : Optional[str]
    createat : datetime
    
    
class Config: #เพื่อให้สามารถอ่านข้อมูลจาก DB Model ได้โดยตรง
        from_attributes = True

    
    
    