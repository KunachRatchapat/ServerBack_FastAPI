from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

T = TypeVar('T')

#---Login---
class Login(BaseModel):
    email: str
    password: str
    
#---Register---
class Register(BaseModel):
    username: str
    password: str
    email: str
    surname: str
    
#--ResponeSchema---
class ResponseSchema(BaseModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T] = None
    
#---Token---
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
