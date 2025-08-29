from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from repository.jwt_repo import JWTRepo
from repository.users_repo import UsersRepo
from db.database import get_session
from db.models.user_model import Users
from typing import Optional, Dict, Any

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authentication/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    payload: Dict[str, Any] = JWTRepo.decode_token(token=token)
    
    # --- ตรวจสอบว่า payload ว่างหรือไม่ (Token ไม่ถูกต้อง/หมดอายุ) ---
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # ---  ดึง username และ role จาก payload ---
    username: Optional[str] = payload.get("sub")
    role_from_token : Optional[str] = payload.get("role")
    
    # --- **เพิ่มการตรวจสอบตรงนี้** เพื่อให้แน่ใจว่า username ไม่ใช่ None ---
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    #--- เมื่อแน่ใจว่า username เป็น str แล้ว ค่อยเรียกใช้ฟังก์ชันค้นหา ---
    user = UsersRepo.find_by_username(db, username=username)
    
    #--- No Users ---
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    #--- Check role Token in like Database ---
    if user.role != role_from_token:
        raise HTTPException(status_code=401, detail="Invalid Token: role mismatch")
    
    return user

def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user