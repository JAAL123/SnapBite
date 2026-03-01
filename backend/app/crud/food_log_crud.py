from uuid import UUID
from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.user import User
from sqlalchemy import func, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.food_log import FoodLog
from app.schemas.food_log_scheema import FoodLogCreate


async def create_food_log(
    db: AsyncSession, food_log: FoodLogCreate, user_id: UUID
) -> FoodLog:
    db_food_log = FoodLog(**food_log.model_dump(), user_id=user_id)
    db.add(db_food_log)
    await db.commit()
    await db.refresh(db_food_log)
    return db_food_log


async def get_food_logs(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[FoodLog]:
    result = await db.execute(select(FoodLog).offset(skip).limit(limit))
    return result.scalars().all()


async def get_daily_summary_by_user(db: AsyncSession, user_id: UUID) -> dict:
    sv_tz = ZoneInfo("America/El_Salvador")
    today = datetime.now(sv_tz).date()

    created_at_sv = func.timezone(
        "America/El_Salvador", func.timezone("UTC", FoodLog.created_at)
    )

    query = select(
        func.sum(FoodLog.calories).label("total_calories"),
        func.sum(FoodLog.proteins).label("total_proteins"),
        func.sum(FoodLog.carbs).label("total_carbs"),
        func.sum(FoodLog.fats).label("total_fats"),
    ).where(FoodLog.user_id == user_id, cast(created_at_sv, Date) == today)

    result = await db.execute(query)
    totals = result.one()

    return {
        "total_calories": totals.total_calories or 0.0,
        "total_proteins": totals.total_proteins or 0.0,
        "total_carbs": totals.total_carbs or 0.0,
        "total_fats": totals.total_fats or 0.0,
    }


async def update_daily_goal(
    db: AsyncSession, user_id: UUID, new_goal: float
) -> User | None:

    user = await db.get(User, user_id)

    if not user:
        return None

    user.daily_calory_goal = new_goal

    await db.commit()
    await db.refresh(user)

    return user
