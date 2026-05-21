from fastapi import HTTPException
from sqlmodel import Session

from app.core.pagination import PaginatedResult, paginate
from app.domains.fruit.repository import FruitRepository
from app.domains.fruit.schemas import FruitCreate, FruitUpdate
from db.models.fruit_model import Fruit


class FruitService:
    def __init__(self) -> None:
        self.repo = FruitRepository()

    def list(
        self, db: Session, offset: int = 0, limit: int = 100
    ) -> list[Fruit]:
        return self.repo.list(db, offset, limit)

    def paginate(
        self, db: Session, page: int = 1, size: int = 10, base_path: str = ""
    ) -> PaginatedResult:
        return paginate(self.repo, db, page, size, base_path)

    def get(self, db: Session, fruit_id: int) -> Fruit:
        fruit = self.repo.get(db, fruit_id)
        if not fruit:
            raise HTTPException(status_code=404, detail="Fruit not found")
        return fruit

    def create(self, db: Session, data: FruitCreate) -> Fruit:
        fruit = Fruit(**data.model_dump())
        return self.repo.create(db, fruit)

    def update(self, db: Session, fruit_id: int, data: FruitUpdate) -> Fruit:
        updated = self.repo.update(db, fruit_id, data.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail="Fruit not found")
        return updated

    def delete(self, db: Session, fruit_id: int) -> None:
        if not self.repo.delete(db, fruit_id):
            raise HTTPException(status_code=404, detail="Fruit not found")
