from app.core.repository import SQLModelRepository
from db.models.fruit_model import Fruit


class FruitRepository(SQLModelRepository[Fruit]):
    def __init__(self):
        super().__init__(Fruit)
