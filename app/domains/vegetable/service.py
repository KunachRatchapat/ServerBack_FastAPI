from fastapi import HTTPException
from sqlmodel import Session

from app.core.pagination import PaginatedResult, paginate
from app.domains.vegetable.repository import VegetableRepository
from app.domains.vegetable.schemas import VegetableCreate, VegetableUpdate
from db.models.vegetable_model import Vegetable


class VegetableService:
    def __init__(self) -> None:
        self.repo = VegetableRepository()

    def list(self, db: Session, offset: int = 0, limit: int = 100) -> list[Vegetable]:
        return self.repo.list(db, offset, limit)

    def paginate(
        self, db: Session, page: int = 1, size: int = 10, base_path: str = ""
    ) -> PaginatedResult:
        return paginate(self.repo, db, page, size, base_path)

    def get(self, db: Session, vegetable_id: int) -> Vegetable:
        veg = self.repo.get(db, vegetable_id)
        if not veg:
            raise HTTPException(status_code=404, detail="Vegetable not found")
        return veg

    def create(self, db: Session, data: VegetableCreate) -> Vegetable:
        veg = Vegetable(**data.model_dump())
        return self.repo.create(db, veg)

    def update(self, db: Session, vegetable_id: int, data: VegetableUpdate) -> Vegetable:
        updated = self.repo.update(db, vegetable_id, data.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail="Vegetable not found")
        return updated

    def delete(self, db: Session, vegetable_id: int) -> None:
        if not self.repo.delete(db, vegetable_id):
            raise HTTPException(status_code=404, detail="Vegetable not found")
