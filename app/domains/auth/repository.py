from typing import Optional

from sqlmodel import Session, select

from app.core.repository import SQLModelRepository
from db.models.user_model import Users


class UserRepository(SQLModelRepository[Users]):
    def __init__(self):
        super().__init__(Users)

    def find_by_email(self, db: Session, email: str) -> Optional[Users]:
        stmt = select(Users).where(Users.email == email)
        stmt = self._exclude_deleted(stmt)
        return db.exec(stmt).first()
