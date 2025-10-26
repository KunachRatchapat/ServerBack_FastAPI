from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from repository.jwt import JWTRepo
from repository.users import UsersRepo
from db.database import get_session
from db.models.user_model import Users
from typing import Optional, Dict, Any

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authentication/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    payload = JWTRepo.decode_token(token=token)
    
    # -- Check payload --
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # -- ดึง username และ role จาก payload --
    user_email: Optional[str] = payload.get("sub")
   
    
    #-- เช็คด้วยว่า user มีไรส่งมาไหม --
    if user_email is None:
        raise HTTPException(status_code=401, detail="Invalid token payload: 'sub' not found")


    user = UsersRepo.find_by_email(db, email=user_email)
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
   
    return user

#สิทธิ์แอดมิน
def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user