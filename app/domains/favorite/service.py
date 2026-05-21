from sqlmodel import Session

from app.domains.favorite.repository import FavoriteRepository
from app.domains.favorite.schemas import FavoriteItemResponse, FavoriteToggle
from db.models.favorite_model import Favorite


class FavoriteService:
    def __init__(self) -> None:
        self.repo = FavoriteRepository()

    def toggle(self, db: Session, user_id: int, data: FavoriteToggle) -> dict:
        existing = self.repo.find_by_user_and_item(
            db, user_id, data.vegetable_id, data.fruit_id
        )
        if existing:
            db.delete(existing)
            db.commit()
            return {"message": "Unfavorite Success"}

        fav = Favorite(
            users_id=user_id,
            vegetable_id=data.vegetable_id,
            fruit_id=data.fruit_id,
        )
        self.repo.create(db, fav)
        return {"message": "Favorite Success"}

    def get_favorites(self, db: Session, user_id: int) -> list[FavoriteItemResponse]:
        favorites = self.repo.find_by_user_with_items(db, user_id)
        result = []
        for f in favorites:
            if f.vegetable_id and f.vegetable:
                result.append(FavoriteItemResponse(
                    id=f.id,
                    user_id=f.users_id,
                    type="vegetable",
                    item_id=f.vegetable.id,
                    item_name=f.vegetable.name,
                    item_description=f.vegetable.description,
                    item_image_url=f.vegetable.picture,
                    createat=f.createat,
                ))
            elif f.fruit_id and f.fruit:
                result.append(FavoriteItemResponse(
                    id=f.id,
                    user_id=f.users_id,
                    type="fruit",
                    item_id=f.fruit.id,
                    item_name=f.fruit.name,
                    item_description=f.fruit.description,
                    item_image_url=f.fruit.picture,
                    createat=f.createat,
                ))
        return result
