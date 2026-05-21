from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUserDep, SessionDep
from app.core.response import success_response
from app.domains.favorite.schemas import FavoriteToggle
from app.domains.favorite.service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["Favorites"])


def get_favorite_service() -> FavoriteService:
    return FavoriteService()


FavoriteServiceDep = Annotated[FavoriteService, Depends(get_favorite_service)]


@router.post("/toggle")
def toggle_favorite(
    db: SessionDep, service: FavoriteServiceDep, current_user: CurrentUserDep, data: FavoriteToggle,
):
    result = service.toggle(db, current_user.id, data)
    return success_response(result, result["message"])


@router.get("/")
def list_favorites(db: SessionDep, service: FavoriteServiceDep, current_user: CurrentUserDep):
    items = service.get_favorites(db, current_user.id)
    return success_response(items)
