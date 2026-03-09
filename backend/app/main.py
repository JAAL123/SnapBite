from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import engine
from app.models import Base, User, FoodLog, AiAudit
from app.api.api import api_router
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando App")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas")
    yield


app = FastAPI(title="SnapBite API", version="0.1.0", lifespan=lifespan)

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "API de SnapBite, status: 'OK'"}


@app.get("/health")
async def health():
    return {"status": "OK"}
