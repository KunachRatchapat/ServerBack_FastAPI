from app.core.repository import SQLModelRepository
from db.models.vegetable_model import Vegetable


class VegetableRepository(SQLModelRepository[Vegetable]):
    def __init__(self):
        super().__init__(Vegetable)
