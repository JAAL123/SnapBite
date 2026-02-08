from fastapi import APIRouter
from app.api.endpoints.food_log import router as food_log_router

api_router = APIRouter()

api_router.include_router(food_log_router, prefix="/food-logs", tags=["food_logs"])
