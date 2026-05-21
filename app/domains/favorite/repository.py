from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.repository import SQLModelRepository
from db.models.favorite_model import Favorite


class FavoriteRepository(SQLModelRepository[Favorite]):
    def __init__(self):
        super().__init__(Favorite)

    def find_by_user_and_item(
        self, db: Session, user_id: int, vegetable_id: Optional[int], fruit_id: Optional[int]
    ) -> Optional[Favorite]:
        stmt = select(Favorite).where(Favorite.users_id == user_id)
        if vegetable_id:
            stmt = stmt.where(Favorite.vegetable_id == vegetable_id)
        if fruit_id:
            stmt = stmt.where(Favorite.fruit_id == fruit_id)
        return db.exec(stmt).first()

    def find_by_user_with_items(self, db: Session, user_id: int) -> list[Favorite]:
        stmt = (
            select(Favorite)
            .where(Favorite.users_id == user_id)
            .options(selectinload(Favorite.vegetable), selectinload(Favorite.fruit))
        )
        return db.exec(stmt).all()
