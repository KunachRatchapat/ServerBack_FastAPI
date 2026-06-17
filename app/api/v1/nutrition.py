from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.api.deps import AdminUserDep, SessionDep
from app.core.response import created_response, success_response
from app.domains.nutrition.schemas import NutritionCreate, NutritionResponse, NutritionUpdate
from app.domains.nutrition.service import NutritionService

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


def get_nutrition_service() -> NutritionService:
    return NutritionService()


NutritionServiceDep = Annotated[NutritionService, Depends(get_nutrition_service)]


@router.get("/")
def list_nutrition(
    request: Request,
    db: SessionDep,
    service: NutritionServiceDep,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    result = service.paginate(db, page, size, request.url.path)
    return success_response(result)


@router.get("/{nutrition_id}")
def get_nutrition(db: SessionDep, service: NutritionServiceDep, nutrition_id: int):
    obj = service.get(db, nutrition_id)
    return success_response(NutritionResponse.model_validate(obj))


@router.get("/fruit/{fruit_id}")
def get_nutrition_by_fruit(db: SessionDep, service: NutritionServiceDep, fruit_id: int):
    obj = service.get_by_fruit(db, fruit_id)
    return success_response(obj)


@router.get("/vegetable/{vegetable_id}")
def get_nutrition_by_vegetable(
    db: SessionDep, service: NutritionServiceDep, vegetable_id: int
):
    obj = service.get_by_vegetable(db, vegetable_id)
    return success_response(obj)


@router.post("/", status_code=201)
def create_nutrition(
    db: SessionDep,
    service: NutritionServiceDep,
    admin: AdminUserDep,
    data: NutritionCreate,
):
    obj = service.create(db, data)
    return created_response(NutritionResponse.model_validate(obj))


@router.put("/{nutrition_id}")
def update_nutrition(
    db: SessionDep,
    service: NutritionServiceDep,
    admin: AdminUserDep,
    nutrition_id: int,
    data: NutritionUpdate,
):
    obj = service.update(db, nutrition_id, data)
    return success_response(NutritionResponse.model_validate(obj))


@router.delete("/{nutrition_id}", status_code=204)
def delete_nutrition(
    db: SessionDep,
    service: NutritionServiceDep,
    admin: AdminUserDep,
    nutrition_id: int,
):
    service.delete(db, nutrition_id)
