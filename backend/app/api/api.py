from fastapi import APIRouter
from app.api.endpoints import food_log, login, users


api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(food_log.router, prefix="/food-logs", tags=["Food Logs"])
