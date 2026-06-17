from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.api.deps import AdminUserDep, SessionDep
from app.core.response import created_response, success_response
from app.domains.vegetable.schemas import VegetableCreate, VegetableUpdate
from app.domains.vegetable.service import VegetableService

router = APIRouter(prefix="/vegetables", tags=["Vegetables"])


def get_vegetable_service() -> VegetableService:
    return VegetableService()


VegetableServiceDep = Annotated[VegetableService, Depends(get_vegetable_service)]


@router.get("/")
def list_vegetables(
    request: Request,
    db: SessionDep,
    service: VegetableServiceDep,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    result = service.paginate(db, page, size, request.url.path)
    return success_response(result)


@router.get("/{vegetable_id}")
def get_vegetable(db: SessionDep, service: VegetableServiceDep, vegetable_id: int):
    veg = service.get(db, vegetable_id)
    return success_response(veg)


@router.post("/", status_code=201)
def create_vegetable(
    db: SessionDep,
    service: VegetableServiceDep,
    admin: AdminUserDep,
    data: VegetableCreate,
):
    veg = service.create(db, data)
    return created_response(veg)


@router.put("/{vegetable_id}")
def update_vegetable(
    db: SessionDep,
    service: VegetableServiceDep,
    admin: AdminUserDep,
    vegetable_id: int,
    data: VegetableUpdate,
):
    veg = service.update(db, vegetable_id, data)
    return success_response(veg)


@router.delete("/{vegetable_id}", status_code=204)
def delete_vegetable(
    db: SessionDep,
    service: VegetableServiceDep,
    admin: AdminUserDep,
    vegetable_id: int,
):
    service.delete(db, vegetable_id)
