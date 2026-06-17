from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.api.deps import AdminUserDep, SessionDep
from app.core.response import success_response
from app.domains.admin.schemas import UserUpdate
from app.domains.admin.service import AdminService
from app.domains.auth.schemas import UserResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_admin_service() -> AdminService:
    return AdminService()


AdminServiceDep = Annotated[AdminService, Depends(get_admin_service)]


@router.get("/users")
def list_users(
    request: Request,
    db: SessionDep,
    service: AdminServiceDep,
    admin: AdminUserDep,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    result = service.paginate(db, page, size, request.url.path)
    return success_response(result)


@router.get("/users/{user_id}")
def get_user(db: SessionDep, service: AdminServiceDep, admin: AdminUserDep, user_id: int):
    user = service.get_user(db, user_id)
    return success_response(UserResponse.model_validate(user))


@router.put("/users/{user_id}")
def update_user(
    db: SessionDep, service: AdminServiceDep, admin: AdminUserDep,
    user_id: int, data: UserUpdate,
):
    user = service.update_user(db, user_id, data)
    return success_response(UserResponse.model_validate(user))


@router.get("/stats")
def get_stats(
    db: SessionDep, service: AdminServiceDep, admin: AdminUserDep,
):
    stats = service.get_stats(db)
    return success_response(stats)


@router.delete("/users/{user_id}")
def delete_user(
    db: SessionDep, service: AdminServiceDep, admin: AdminUserDep, user_id: int,
):
    service.delete_user(db, user_id)
    return success_response(message="User deleted")
