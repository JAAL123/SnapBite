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


class MacrosResponse(BaseModel):
    calories: float
    proteins: float
    carbs: float
    fats: float


class DailySummaryResponse(BaseModel):
    daily_goal: float
    consumed_calories: float
    remaining_calories: float
    macros: MacrosResponse


class GoalUpdateRequest(BaseModel):
    new_goal: float


class GoalUpdateResponse(BaseModel):
    message: str
    new_goal: float
