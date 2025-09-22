from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Annotated
from db.database import get_session
from db.models.user_model import Users
from repository.users import UsersRepo
from depencies.dependencies import get_current_admin_user
from pydantic import BaseModel

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]
AdminUserDep = Annotated[Users, Depends(get_current_admin_user)]

# -- Schema สำหรับการอัปเดตข้อมูลผู้ใช้ --
class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    role: str | None = None


#-- ดึงข้อมูล users ทั้งหมด --
@router.get("/admin/users", response_model=List[Users])
def get_all_users(session: SessionDep, admin: AdminUserDep):
    users = session.exec(select(Users)).all()
    return users


#-- ดึงข้อมูล user สักคนมาดู --
@router.get("/admin/users/{user_id}", response_model=Users)
def get_user_by_id(user_id: int, session: SessionDep, admin: AdminUserDep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


#-- อัปเดตข้อมูล --
@router.put("/admin/users/{user_id}", response_model=Users)
def update_user(user_id: int, user_data: UserUpdate, session: SessionDep, admin: AdminUserDep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # -- อัปเดตเฉพาะข้อมูลที่มีการเปลี่ยนแปลง --
    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# --ลบใครสักคนออกจากแอป --
@router.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep, admin: AdminUserDep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}
