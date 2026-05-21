from typing import Optional

from sqlmodel import Session, select

from app.core.repository import SQLModelRepository
from db.models.user_model import Users


class UserRepository(SQLModelRepository[Users]):
    def __init__(self):
        super().__init__(Users)

    def find_by_email(self, db: Session, email: str) -> Optional[Users]:
        return db.exec(select(Users).where(Users.email == email)).first()
