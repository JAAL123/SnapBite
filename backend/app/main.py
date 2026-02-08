from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import engine
from app.models import Base, User, FoodLog, AiAudit
from app.api.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando App")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas")
    yield


app = FastAPI(title="SnapBite API", version="0.1.0", lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "API de SnapBite, status: 'OK'"}


@app.get("/health")
async def health():
    return {"status": "OK"}
