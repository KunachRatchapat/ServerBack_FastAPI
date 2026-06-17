from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.api.deps import AdminUserDep, SessionDep
from app.core.response import created_response, success_response
from app.domains.fruit.schemas import FruitCreate, FruitResponse, FruitUpdate
from app.domains.fruit.service import FruitService

router = APIRouter(prefix="/fruits", tags=["Fruits"])


def get_fruit_service() -> FruitService:
    return FruitService()


FruitServiceDep = Annotated[FruitService, Depends(get_fruit_service)]


@router.get("/")
def list_fruits(
    request: Request,
    db: SessionDep,
    service: FruitServiceDep,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    result = service.paginate(db, page, size, request.url.path)
    return success_response(result)


@router.get("/{fruit_id}")
def get_fruit(db: SessionDep, service: FruitServiceDep, fruit_id: int):
    fruit = service.get(db, fruit_id)
    return success_response(FruitResponse.model_validate(fruit))


@router.post("/", status_code=201)
def create_fruit(
    db: SessionDep,
    service: FruitServiceDep,
    admin: AdminUserDep,
    data: FruitCreate,
):
    fruit = service.create(db, data)
    return created_response(FruitResponse.model_validate(fruit))


@router.put("/{fruit_id}")
def update_fruit(
    db: SessionDep,
    service: FruitServiceDep,
    admin: AdminUserDep,
    fruit_id: int,
    data: FruitUpdate,
):
    fruit = service.update(db, fruit_id, data)
    return success_response(FruitResponse.model_validate(fruit))


@router.delete("/{fruit_id}", status_code=204)
def delete_fruit(
    db: SessionDep,
    service: FruitServiceDep,
    admin: AdminUserDep,
    fruit_id: int,
):
    service.delete(db, fruit_id)
