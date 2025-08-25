from fastapi import APIRouter, Depends
from sqlmodel import  Session
from schema.users import ResponseSchema, Login, TokenRespone,Register
from passlib.context import CryptContext
from repository.users_repo import UsersRepo
from db.models.user_model import Users
from db.database import get_session

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

#---Register---
@router.post('/Authentication/signup')
def signup(request: Register, db: Session = Depends(get_session)):
    try:
        #---Hash Password---
        hashed_password = pwd_context.hash(request.password)
        
        #insert data
        _user = Users(
            email = request.email,
            password = hashed_password,
            name = request.username,
            surname = request.surname
        )
        UsersRepo.insert(db,_user)
        
        return ResponseSchema(
            code="200", 
            status="Ok", 
            message="Success save Data"
            ).dict(exclude_none=True)
    
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500", 
            status="Error",
            message="Internal Server Error"
            ).dict(exclude_none=True)






    
    