from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.food_log import Source


class FoodLogBase(BaseModel):
    food_name: str
    calories: float
    proteins: float = 0.0
    carbs: float = 0.0
    fats: float = 0.0
    image_url: Optional[str] = None
    source: Source = Source.WEB


class FoodLogCreate(FoodLogBase):
    pass


class FoodLogResponse(FoodLogBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
