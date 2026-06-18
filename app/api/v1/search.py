from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import SessionDep
from app.core.response import success_response
from app.domains.search.service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])


def get_search_service() -> SearchService:
    return SearchService()


SearchServiceDep = Annotated[SearchService, Depends(get_search_service)]


@router.get("/")
def search(
    db: SessionDep,
    service: SearchServiceDep,
    keyword: str = Query(..., description="Search fruits and vegetables by name"),
):
    results = service.search(db, keyword)
    return success_response(results)
