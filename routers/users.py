from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from schema.users_schema import ResponseSchema, Login, TokenResponse, Register
from passlib.context import CryptContext
from repository.users import UsersRepo
from repository.jwt import JWTRepo
from db.models.user_model import Users
from db.database import get_session
from depencies.dependencies import get_current_user

router = APIRouter()

pwd_context = CryptContext(schemes=['argon2'], deprecated="auto")
SessionDep = Annotated[Session, Depends(get_session)]

#--- สมัคร ---
@router.post('/Authentication/signup', response_model=ResponseSchema)
def signup(request: Register, db: SessionDep):
    already_user = UsersRepo.find_by_email(db, request.email)
    if already_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    
    #-- Hash password --
   
    hashed_pass = pwd_context.hash(request.password)
    
    _user = Users(
        email=request.email,
        password=hashed_pass,
        username=request.username,
        surname=request.surname,
        role="user" # ทุกคนเข้ามาจะให้ role นี้ก่อนนะครับ
    )
    
    UsersRepo.insert(db, _user)
    
    return ResponseSchema(
        code=str(status.HTTP_201_CREATED),
        status="Created",
        message="User created successfully"
    )

#--- ล็อกอิน ---
@router.post('/Authentication/login', response_model=ResponseSchema)
def login(request: Login, db: SessionDep):
    _user = UsersRepo.find_by_email(db, request.email)
    
    if not _user or not pwd_context.verify(request.password, _user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    #-- Generate Token
    token_data = {"sub": _user.email, "role": _user.role}
    token = JWTRepo.generate_token(data=token_data)
    
    return ResponseSchema(
        code=str(status.HTTP_200_OK),
        status="OK",
        message="Login Successful",
        result=TokenResponse(access_token=token, token_type="bearer")
    )

#--- ล็อคเอ้าต์ ---
@router.post("/Authentication/logout", response_model=ResponseSchema)
def logout(current_user: Users = Depends(get_current_user)):
    return ResponseSchema(
        code=str(status.HTTP_200_OK),
        status="Ok",
        message="Logout successful"
    )