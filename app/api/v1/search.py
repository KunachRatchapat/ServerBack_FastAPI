
from fastapi import APIRouter, Query
from sqlmodel import col, select

from app.api.deps import SessionDep
from app.core.response import success_response
from db.models.fruit_model import Fruit
from db.models.vegetable_model import Vegetable

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
def search(
    db: SessionDep,
    keyword: str = Query(..., description="Search fruits and vegetables by name"),
):
    fruits = db.exec(
        select(Fruit)
        .where(col(Fruit.name).ilike(f"%{keyword}%"), Fruit.deleteat.is_(None))
    ).all()
    vegs = db.exec(
        select(Vegetable)
        .where(col(Vegetable.name).ilike(f"%{keyword}%"), Vegetable.deleteat.is_(None))
    ).all()
    results = [{"name": f.name} for f in fruits] + [{"name": v.name} for v in vegs]
    return success_response(results)
