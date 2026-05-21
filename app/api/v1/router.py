from fastapi import APIRouter

from app.api.v1 import (
    admin,
    auth,
    favorites,
    fruits,
    nutrition,
    prediction,
    search,
    upload,
    vegetables,
)

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(fruits.router)
v1_router.include_router(vegetables.router)
v1_router.include_router(prediction.router)
v1_router.include_router(auth.router)
v1_router.include_router(favorites.router)
v1_router.include_router(admin.router)
v1_router.include_router(search.router)
v1_router.include_router(upload.router)
v1_router.include_router(nutrition.router)
