from datetime import datetime, timedelta 
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette import status
from db.models.user_model import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from jose import jwt,JWTError
import os
from dotenv import load_dotenv


router = APIRouter(prefix='/auth',tags=['auth'])

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'] ,deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


@router.post("/register")
def register(user: UsersCreate , session: Session = SessionDep):
    already_user = session.exec(
        select(Users).where(Users.email == user.email)
    )
    