from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class NutritionCreate(BaseModel):
    fruit_id: Optional[int] = None
    vegetable_id: Optional[int] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None

    @model_validator(mode="after")
    def check_exactly_one_target(self):
        has_fruit = self.fruit_id is not None
        has_vegetable = self.vegetable_id is not None
        if has_fruit == has_vegetable:
            raise ValueError("Exactly one of fruit_id or vegetable_id must be provided")
        return self


class NutritionUpdate(BaseModel):
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None


class NutritionResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    fruit_id: Optional[int] = None
    vegetable_id: Optional[int] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    createat: datetime
