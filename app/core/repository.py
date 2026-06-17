from datetime import datetime, timezone
from typing import Generic, Optional, Protocol, TypeVar

from sqlmodel import Session, SQLModel, func, select

from app.config import settings

ModelT = TypeVar("ModelT", bound=SQLModel)


class RepositoryProtocol(Protocol[ModelT]):
    def get(self, db: Session, id: int) -> Optional[ModelT]: ...
    def list(self, db: Session, offset: int, limit: int) -> list[ModelT]: ...
    def create(self, db: Session, data: ModelT) -> ModelT: ...
    def update(self, db: Session, id: int, data: dict) -> Optional[ModelT]: ...
    def delete(self, db: Session, id: int) -> bool: ...


class HasDeleteAt:
    deleteat: Optional[datetime]


class SQLModelRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT]):
        self._model = model

    def _exclude_deleted(self, stmt):
        if hasattr(self._model, "deleteat"):
            col = getattr(self._model, "deleteat")
            return stmt.where(col.is_(None))
        return stmt

    def get(self, db: Session, id: int) -> Optional[ModelT]:
        obj = db.get(self._model, id)
        if obj is None:
            return None
        if hasattr(self._model, "deleteat") and getattr(obj, "deleteat") is not None:
            return None
        return obj

    def list(
        self, db: Session, offset: int = 0, limit: int = settings.DEFAULT_LIST_LIMIT
    ) -> list[ModelT]:
        stmt = select(self._model)
        stmt = self._exclude_deleted(stmt)
        stmt = stmt.offset(offset).limit(limit)
        return db.exec(stmt).all()

    def count(self, db: Session) -> int:
        stmt = select(func.count()).select_from(self._model)
        stmt = self._exclude_deleted(stmt)
        return db.exec(stmt).one()

    def create(self, db: Session, data: ModelT) -> ModelT:
        if hasattr(data, "createat") and getattr(data, "createat") is None:
            data.createat = datetime.now(timezone.utc)
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    def update(self, db: Session, id: int, data: dict) -> Optional[ModelT]:
        obj = self.get(db, id)
        if not obj:
            return None
        if hasattr(obj, "updateat"):
            data["updateat"] = datetime.now(timezone.utc)
        for key, value in data.items():
            setattr(obj, key, value)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> bool:
        obj = self.get(db, id)
        if not obj:
            return False
        if hasattr(obj, "deleteat"):
            obj.deleteat = datetime.now(timezone.utc)
            db.add(obj)
            db.commit()
            return True
        db.delete(obj)
        db.commit()
        return True
