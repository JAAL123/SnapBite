from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.services.cloudinary import upload_image
from app.models.user import User
from app.core.database import get_db
from app.api import dependencies
from app.schemas.food_log_scheema import (
    FoodLogCreate,
    FoodLogResponse,
    DailySummaryResponse,
    GoalUpdateResponse,
    MacrosResponse,
    GoalUpdateRequest,
)
from app.crud.food_log_crud import (
    create_food_log,
    get_food_logs,
    get_daily_summary_by_user,
    update_daily_goal,
    delete_food_log_by_user,
)

router = APIRouter()


@router.get("/", response_model=List[FoodLogResponse])
async def read_food_logs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(dependencies.get_current_user),
):
    food_logs = await get_food_logs(
        db,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
    )
    return food_logs


@router.post("/", response_model=FoodLogResponse)
async def create_food_log_endpoint(
    food_log: FoodLogCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user=Depends(dependencies.get_current_user),
):
    return await create_food_log(db, food_log, user_id=current_user.id)


@router.get(
    "/telegram/{telegram_id}/summary/today", response_model=DailySummaryResponse
)
async def get_telegram_daily_summary(
    telegram_id: int, db: Annotated[AsyncSession, Depends(get_db)]
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
            calories=consumed,
            proteins=totals["total_proteins"],
            carbs=totals["total_carbs"],
            fats=totals["total_fats"],
        ),
    )


@router.patch("/telegram/{telegram_id}/goal")
async def update_user_goal(
    telegram_id: int,
    request: GoalUpdateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    query = select(User).where(User.telegram_id == telegram_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario de Telegram no encontrado")

    updated_user = await update_daily_goal(
        db=db, user_id=user.id, new_goal=request.new_goal
    )

    return GoalUpdateResponse(
        message="Goal Updated", new_goal=updated_user.daily_calory_goal
    )


@router.delete("/telegram/{telegram_id}/log/{log_id}")
async def delete_telegram_log(
    telegram_id: int, log_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    query_user = select(User).where(User.telegram_id == telegram_id)
    result_user = await db.execute(query_user)
    user = result_user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success = await delete_food_log_by_user(db=db, log_id=log_id, user_id=user.id)

    if not success:
        raise HTTPException(
            status_code=404, detail="Register not found or not authorized to delete"
        )

    return {"message": "Register deleted successfully"}


@router.post("/upload", response_model=FoodLogResponse)
async def upload_food_web(
    food_name: str = Form(...),
    calories: float = Form(...),
    proteins: float = Form(...),
    carbs: float = Form(...),
    fats: float = Form(...),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(dependencies.get_current_user),
):
    image_url = None

    if file:
        image_url = await upload_image(file.file)
        if not image_url:
            raise HTTPException(status_code=500, detail="Image processing error")

    food_log_in = FoodLogCreate(
        food_name=food_name,
        calories=calories,
        proteins=proteins,
        carbs=carbs,
        fats=fats,
        image_url=image_url,
    )

    return await create_food_log(db, food_log_in, user_id=current_user.id)
