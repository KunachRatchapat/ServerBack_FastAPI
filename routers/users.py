from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from schema.users import ResponseSchema, Login, TokenResponse,Register
from passlib.context import CryptContext
from repository.users_repo import UsersRepo
from repository.jwt_repo import JWTRepo
from db.models.user_model import Users
from db.database import get_session
from datetime import timedelta, datetime


router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

#--- Register ---
@router.post('/Authentication/signup',response_model=ResponseSchema)
def signup(request: Register, db: Session = Depends(get_session)):
    try:
        
        # Check if username or email already exists to prevent duplication
        if UsersRepo.find_by_username(db, request.username) or UsersRepo.find_by_email(db, request.email):
            raise HTTPException(status_code=409, detail="Username or email already exists")
        
        #--- Hash Password ---
        hashed_password = pwd_context.hash(request.password)
        
        #--- insert data ---
        _user = Users(
            email = request.email,
            password = hashed_password,
            username = request.username,
            surname = request.surname
        )
        UsersRepo.insert(db,_user)
        
        return ResponseSchema(
            code="200", 
            status="Ok", 
            message="User Create successfully"
        )
    
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        print(f"Error during signup: {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


#--- Login ---
@router.post('/Authentication/login',response_model=ResponseSchema)
def login(request: Login, db: Session = Depends(get_session)):
    try:
        #--- Find by Username ---
        _user = UsersRepo.find_by_email(db,request.email) 
        
           #--- Check if user exists and verify password ---
        if not _user or not pwd_context.verify(request.password, _user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
         # --- Generate token ---
        token_data = {"sub": _user.username , "role":_user.role}
        token = JWTRepo.generate_token(data=token_data)
        
        #--- Return success response with token ---
        return ResponseSchema(
            code="200",
            status="Ok",
            message="Login successful",
            result=TokenResponse(access_token=token, token_type="bearer")
        )
            
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        print(f"Error during login: {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


    
    