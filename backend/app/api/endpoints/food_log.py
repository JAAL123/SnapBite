from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.database import get_db
from app.api import dependencies
from app.schemas.food_log_scheema import FoodLogCreate, FoodLogResponse, DailySummaryResponse, MacrosResponse
from app.crud.food_log_crud import create_food_log, get_food_logs, get_daily_summary_by_user

router = APIRouter()


@router.get("/", response_model=List[FoodLogResponse])
async def read_food_logs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(dependencies.get_current_user),
):
    food_logs = await get_food_logs(db, skip=skip, limit=limit)
    return food_logs


@router.post("/", response_model=FoodLogResponse)
async def create_food_log_endpoint(
    food_log: FoodLogCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user=Depends(dependencies.get_current_user),
):
    return await create_food_log(db, food_log, user_id=current_user.id)


@router.get("/telegram/{telegram_id}/summary/today", response_model=DailySummaryResponse)
async def get_telegram_daily_summary(
    telegram_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):

    query = select(User).where(User.telegram_id == telegram_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario de Telegram no encontrado")

    totals = await get_daily_summary_by_user(db=db, user_id=user.id)

    consumed = totals["total_calories"]
    
    return DailySummaryResponse(
        daily_goal=user.daily_calory_goal,
        consumed_calories=consumed,
        remaining_calories=user.daily_calory_goal - consumed,
        macros=MacrosResponse(
            proteins=totals["total_proteins"],
            carbs=totals["total_carbs"],
            fats=totals["total_fats"]
        )
    )