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
    
    #---find Email---
    @staticmethod
    def find_by_email(db: Session, email: str) -> Optional[Users]:
        return db.exec(select(Users).where(Users.email == email)).first()
    
    #---find Username---
    @staticmethod
    def find_by_username(db: Session, username: str) -> Optional[Users]:
        return db.exec(select(Users).where(Users.username == username)).first()
