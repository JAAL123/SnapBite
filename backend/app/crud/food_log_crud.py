from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.food_log import FoodLog
from app.schemas.food_log_scheema import FoodLogCreate


async def create_food_log(db: AsyncSession, food_log: FoodLogCreate) -> FoodLog:
    db_food_log = FoodLog(**food_log.model_dump())
    db.add(db_food_log)
    await db.commit()
    await db.refresh(db_food_log)
    return db_food_log


async def get_food_logs(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[FoodLog]:
    result = await db.execute(select(FoodLog).offset(skip).limit(limit))
    return result.scalars().all()
