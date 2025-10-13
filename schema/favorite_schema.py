from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field
from datetime import datetime


#---Request Model---
class FavoriteCreate(BaseModel):
    user_id : int
    vegetable_id : Optional[int] = None
    fruit_id : Optional[int] = None

#เมื่อเพิ่มสำเร็จ
class FavoriteRespone(BaseModel):
    id: Optional[int] = None
    user_id : int
    vegetable_id : Optional[int] = None
    fruit_id : Optional[int] = None
    createat : datetime
    
#---Respone FavoriteItem---
class FavoriteItemRespone(BaseModel):
    id : Optional[int] 
    user_id : int
    type : str
    item_id :Optional[int] = None
    item_name : str
    item_description : Optional[str] = None
    item_image_url : Optional[str] = None
    createat : datetime