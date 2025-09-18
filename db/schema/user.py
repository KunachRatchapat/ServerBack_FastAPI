from pydantic import BaseModel, EmailStr

#--Create User--
class UsersCreate(BaseModel):
    email: str
    password : str
    name : str
    surname : str
    
#--User Login--
class UsersLogin(BaseModel):
    email: EmailStr
    password : str
    
#--User InDB--    
class UserInDB(BaseModel):
    hash_password : str

#--Token--
class Token(BaseModel):
    access_token : str
    token_type : str
    



    