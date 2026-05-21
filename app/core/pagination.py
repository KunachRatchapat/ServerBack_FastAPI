from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from sqlmodel import Session

from app.core.repository import SQLModelRepository

T = TypeVar("T")


class PaginatedResult(BaseModel, Generic[T]):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[T]


def paginate(
    repo: SQLModelRepository,
    db: Session,
    page: int = 1,
    size: int = 10,
    base_path: str = "",
) -> PaginatedResult:
    offset = (page - 1) * size
    total = repo.count(db)
    items = repo.list(db, offset=offset, limit=size)

    next_url = None
    if offset + size < total:
        next_url = f"{base_path}?page={page + 1}&size={size}"

    prev_url = None
    if page > 1:
        prev_url = f"{base_path}?page={page - 1}&size={size}"

    return PaginatedResult(
        count=total,
        next=next_url,
        previous=prev_url,
        results=items,
    )
