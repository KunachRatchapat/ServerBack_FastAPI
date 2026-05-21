from typing import Optional

from sqlmodel import Session, select

from app.core.repository import SQLModelRepository
from db.models.nutrition_model import Nutrition


class NutritionRepository(SQLModelRepository[Nutrition]):
    def __init__(self):
        super().__init__(Nutrition)

    def find_by_fruit(self, db: Session, fruit_id: int) -> Optional[Nutrition]:
        stmt = select(Nutrition).where(Nutrition.fruit_id == fruit_id)
        return db.exec(stmt).first()

    def find_by_vegetable(self, db: Session, vegetable_id: int) -> Optional[Nutrition]:
        stmt = select(Nutrition).where(Nutrition.vegetable_id == vegetable_id)
        return db.exec(stmt).first()
