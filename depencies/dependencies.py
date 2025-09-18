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
    # ถอดรหัส Token เพื่อดึงข้อมูล payload
    payload: Dict[str, Any] = JWTRepo.decode_token(token=token)
    
    # ตรวจสอบว่า payload ว่างหรือไม่ (ถ้าว่างแสดงว่า Token ไม่ถูกต้อง/หมดอายุ)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # ดึง username และ role จาก payload
    username: Optional[str] = payload.get("sub")
    role_from_token: Optional[str] = payload.get("role")
    
    # ตรวจสอบว่า username มีค่าหรือไม่
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token payload: 'sub' not found")

    # ค้นหาผู้ใช้จากฐานข้อมูล
    user = UsersRepo.find_by_username(db, username=username)
    
    # ถ้าไม่พบผู้ใช้ในฐานข้อมูล
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    # ตรวจสอบว่า role ที่มาจาก Token ตรงกับ role ในฐานข้อมูลหรือไม่
    if user.role != role_from_token:
        # อาจเป็นไปได้ว่า role_from_token เป็น None หรือไม่ตรงกัน
        raise HTTPException(status_code=401, detail="Invalid token: role mismatch")
    
    return user

def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user