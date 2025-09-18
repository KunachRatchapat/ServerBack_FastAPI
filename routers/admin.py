<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Annotated
from db.database import get_session
from db.models.user_model import Users
from repository.users_repo import UsersRepo
from depencies.dependencies import get_current_admin_user
from pydantic import BaseModel

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]
AdminUserDep = Annotated[Users, Depends(get_current_admin_user)]

# Schema สำหรับการอัปเดตข้อมูลผู้ใช้
=======
from fastapi import APIRouter, Depends,HTTPException
from sqlmodel import Session, select
from db.database import get_session
from datetime import datetime, timedelta
from db.models.user_model import Users
from depencies.dependencies import get_current_admin_user
from pydantic import BaseModel
from typing import List, Annotated

router = APIRouter()
SessionDep = Annotated[Session , Depends(get_session)]
AdminUserDep = Annotated[Users, Depends(get_current_admin_user)] #เป็นตัวให้แอดมินเข้าไปค้นหาโดยใช้ยศแอดมิน

>>>>>>> b578e9a0f9f307150eeebbcd174926d8ac20dfda
class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    role: str | None = None

<<<<<<< HEAD
#--- GET /admin/users: ดึงข้อมูลผู้ใช้ทั้งหมด ---
@router.get("/admin/users", response_model=List[Users])
def get_all_users(session: SessionDep, admin: AdminUserDep):
    users = session.exec(select(Users)).all()
    return users

#--- GET /admin/users/{user_id}: ดึงข้อมูลผู้ใช้คนใดคนหนึ่ง ---
@router.get("/admin/users/{user_id}", response_model=Users)
def get_user_by_id(user_id: int, session: SessionDep, admin: AdminUserDep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#--- PUT /admin/users/{user_id}: อัปเดตข้อมูลผู้ใช้ ---
@router.put("/admin/users/{user_id}", response_model=Users)
def update_user(user_id: int, user_data: UserUpdate, session: SessionDep, admin: AdminUserDep):
=======
# --- ดึงข้อมูล User จาก DB ทั้งหมด ---
@router.get("/admin/users",response_model=List[Users])
def get_all_admin(session: Session, admin: AdminUserDep):
    users = session.exec(select(Users)).all()
    return users

# --- ดึงข้อมูล User รายคนงับ ---
@router.get("/admin/users/{user_id}",response_model=Users)
def get_user_by_id(user_id:int, session: SessionDep, admin: AdminUserDep):
>>>>>>> b578e9a0f9f307150eeebbcd174926d8ac20dfda
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
<<<<<<< HEAD
    # อัปเดตเฉพาะข้อมูลที่มีการเปลี่ยนแปลง
    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
=======
# --- อัปเดต User งับบ ---
@router.put("/admind/users/{user_id}", response_model=Users)
def update_user(user_id:int, user_data: UserUpdate, session: SessionDep, admin: AdminUserDep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
        
>>>>>>> b578e9a0f9f307150eeebbcd174926d8ac20dfda
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

<<<<<<< HEAD
#--- DELETE /admin/users/{user_id}: ลบบัญชีผู้ใช้ ---
@router.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep, admin: AdminUserDep):
=======
# --- ลบ User ออกไปป ---
@router.delete("/admin/users/{user_id}")
def delete_user(user_id:int, session: SessionDep, admin: AdminUserDep):
>>>>>>> b578e9a0f9f307150eeebbcd174926d8ac20dfda
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
<<<<<<< HEAD
    return {"message": "User deleted successfully"}
=======
    return{"message": "User deleted success !"}
>>>>>>> b578e9a0f9f307150eeebbcd174926d8ac20dfda
