from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.pagination import PaginatedResult, paginate
from app.domains.nutrition.repository import NutritionRepository
from app.domains.nutrition.schemas import NutritionCreate, NutritionResponse, NutritionUpdate
from db.models.nutrition_model import Nutrition


class NutritionService:
    def __init__(self) -> None:
        self.repo = NutritionRepository()

    def paginate(
        self, db: Session, page: int = 1, size: int = 10, base_path: str = ""
    ) -> PaginatedResult:
        return paginate(self.repo, db, page, size, base_path)

    def get(self, db: Session, nutrition_id: int) -> Nutrition:
        obj = self.repo.get(db, nutrition_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Nutrition not found")
        return obj

    def get_by_fruit(self, db: Session, fruit_id: int) -> NutritionResponse:
        obj = self.repo.find_by_fruit(db, fruit_id)
        if not obj:
            msg = "Nutrition not found for this fruit"
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
        return NutritionResponse.model_validate(obj)

    def get_by_vegetable(self, db: Session, vegetable_id: int) -> NutritionResponse:
        obj = self.repo.find_by_vegetable(db, vegetable_id)
        if not obj:
            msg = "Nutrition not found for this vegetable"
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
        return NutritionResponse.model_validate(obj)

    def create(self, db: Session, data: NutritionCreate) -> Nutrition:
        obj = Nutrition(**data.model_dump())
        return self.repo.create(db, obj)

    def update(self, db: Session, nutrition_id: int, data: NutritionUpdate) -> Nutrition:
        updated = self.repo.update(db, nutrition_id, data.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Nutrition not found")
        return updated

    def delete(self, db: Session, nutrition_id: int) -> None:
        if not self.repo.delete(db, nutrition_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Nutrition not found")
