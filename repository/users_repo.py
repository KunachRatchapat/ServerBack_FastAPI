from typing import Optional
from sqlmodel import Session, select
from db.models.user_model import Users

class BaseRepo:
    @staticmethod
    def insert(db: Session, model: Users) -> Users:
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

class UsersRepo(BaseRepo):
    @staticmethod
    def find_by_email(db: Session, email: str) -> Optional[Users]:
        return db.exec(select(Users).where(Users.email == email)).first()
    
    #---find Name---
    @staticmethod
    def find_by_name(db: Session, name: str) -> Optional[Users]:
        return db.exec(select(Users).where(Users.name == name)).first()
