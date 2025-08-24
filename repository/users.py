from typing import Optional, TypeVar
from sqlmodel import Session, SQLModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

# Load env
load_dotenv()
SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

T = TypeVar("T", bound=SQLModel)

class BaseRepo:
    @staticmethod
    def insert(db: Session, model: T):
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

class UsersRepo(BaseRepo):
    @staticmethod
    def find_by_username(db: Session, model: type[T], username: str) -> Optional[T]:
        return db.query(model).filter(model.username == username).first()

class JWTRepo:
    @staticmethod
    def generate_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
        except JWTError:
            return None
