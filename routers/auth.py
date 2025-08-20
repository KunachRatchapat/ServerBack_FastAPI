from datetime import datetime, timedelta 
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette import status
from db.models.user_model import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from db.schema.user import UsersCreate, UsersLogin
from db.database import get_session   # <- ฟังก์ชันคืน session

router = APIRouter(prefix="/auth", tags=["auth"])

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SessionDep = Annotated[Session, Depends(get_session)]

# Function Hasspassword
def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

@router.post("/register")
def register(user: UsersCreate, session: SessionDep):
    already_user = session.exec(
        select(Users).where(Users.email == user.email)
    ).first()
    
    if already_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #--Hash password User--
    hashed_pass = hash_password(user.password)
    new_user = Users(
        email=user.email,
        password=hashed_pass,
        name=user.name,
        surname=user.surname
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message": "User registered successfully", "user": new_user.email}
