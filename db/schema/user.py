from pydantic import BaseModel, EmailStr

#--Create User--
class UserCreate(BaseModel):
    email: EmailStr
    password : str
    name : str
    surname : str
    
#--User Login--
class UserLogin(BaseModel):
    email: EmailStr
    password : str
    

    

    