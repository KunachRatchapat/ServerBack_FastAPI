from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Nutrition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fruit_id: Optional[int] = Field(default=None, foreign_key="fruit.id", index=True)
    vegetable_id: Optional[int] = Field(default=None, foreign_key="vegetable.id", index=True)
    calories: Optional[float] = Field(default=None)
    protein: Optional[float] = Field(default=None)
    carbs: Optional[float] = Field(default=None)
    fat: Optional[float] = Field(default=None)
    fiber: Optional[float] = Field(default=None)

    createat: datetime = Field(default_factory=datetime.now)
    deleteat: Optional[datetime] = Field(default=None, nullable=True)
    updateat: Optional[datetime] = Field(default=None, nullable=True)
