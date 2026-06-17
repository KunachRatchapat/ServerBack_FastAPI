from fastapi import HTTPException, status
from sqlmodel import Session, func, select

from app.core.pagination import PaginatedResult, paginate
from app.domains.admin.schemas import UserUpdate
from app.domains.auth.repository import UserRepository
from db.models.favorite_model import Favorite
from db.models.fruit_model import Fruit
from db.models.nutrition_model import Nutrition
from db.models.user_model import Users
from db.models.vegetable_model import Vegetable


class AdminService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    def paginate(
        self, db: Session, page: int = 1, size: int = 10, base_path: str = ""
    ) -> PaginatedResult:
        return paginate(self.repo, db, page, size, base_path)

    def get_user(self, db: Session, user_id: int) -> Users:
        user = self.repo.get(db, user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def update_user(self, db: Session, user_id: int, data: UserUpdate) -> Users:
        updated = self.repo.update(db, user_id, data.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated

    def delete_user(self, db: Session, user_id: int) -> None:
        if not self.repo.delete(db, user_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    def _count_active(self, db: Session, model: type) -> int:
        stmt = select(func.count()).select_from(model).where(model.deleteat.is_(None))
        return db.exec(stmt).one()

    def get_stats(self, db: Session) -> dict:
        return {
            "users": self._count_active(db, Users),
            "fruits": self._count_active(db, Fruit),
            "vegetables": self._count_active(db, Vegetable),
            "favorites": self._count_active(db, Favorite),
            "nutrition_records": self._count_active(db, Nutrition),
        }
