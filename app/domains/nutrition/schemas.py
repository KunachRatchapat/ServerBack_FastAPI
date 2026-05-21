from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NutritionCreate(BaseModel):
    fruit_id: Optional[int] = None
    vegetable_id: Optional[int] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None


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
