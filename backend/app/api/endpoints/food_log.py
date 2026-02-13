from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api import dependencies
from app.schemas.food_log_scheema import FoodLogCreate, FoodLogResponse
from app.crud.food_log_crud import create_food_log, get_food_logs

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
