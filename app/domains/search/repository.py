from sqlmodel import Session, col, select

from db.models.fruit_model import Fruit
from db.models.vegetable_model import Vegetable


class SearchRepository:
    def search_fruits(self, db: Session, keyword: str) -> list[Fruit]:
        stmt = (
            select(Fruit)
            .where(col(Fruit.name).ilike(f"%{keyword}%"))
            .where(col(Fruit.deleteat).is_(None))
        )
        return list(db.exec(stmt).all())

    def search_vegetables(self, db: Session, keyword: str) -> list[Vegetable]:
        stmt = (
            select(Vegetable)
            .where(col(Vegetable.name).ilike(f"%{keyword}%"))
            .where(col(Vegetable.deleteat).is_(None))
        )
        return list(db.exec(stmt).all())
