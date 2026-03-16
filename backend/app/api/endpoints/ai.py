import base64
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import UploadFile, File

from app.services.gemini import analyze_food_content
from app.core.database import get_db
from app.crud.user_crud import get_or_create_telegram_user
from app.models.food_log import Source, FoodLog
from app.services.cloudinary import upload_image_base64
from app.api import dependencies
from app.schemas.ai_scheema import TextAnalysisRequest

router = APIRouter()


class AnalysisRequest(BaseModel):
    query: str | None = None
    image_base64: str | None = None
    media_type: str = "image/jpeg"
    telegram_id: int
    first_name: str
    username: str | None = None


@router.post("/analyze")
async def analyze_food(
    request: AnalysisRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    1. Autentica/Crea al usuario de Telegram.
    2. Analiza comida (texto y/o imagen) con Gemini.
    3. Guarda el registro en la base de datos.
    """
    user = await get_or_create_telegram_user(
        db=db,
        telegram_id=request.telegram_id,
        first_name=request.first_name,
        tg_username=request.username,
    )

    image_bytes = None
    if request.image_base64:
        try:
            image_bytes = base64.b64decode(request.image_base64)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")

    if not request.query and not image_bytes:
        raise HTTPException(status_code=400, detail="Provide text query or image")

    ai_result = await analyze_food_content(
        text_query=request.query, image_bytes=image_bytes, mime_type=request.media_type
    )

    if not ai_result:
        raise HTTPException(status_code=500, detail="Could not analyze food with AI")

    uploaded_image_url = None
    if request.image_base64:
        print("☁️ Subiendo imagen a Cloudinary...")
        uploaded_image_url = await upload_image_base64(request.image_base64)

    try:
        food_log_data = FoodLog(
            user_id=user.id,
            food_name=ai_result.get("food_name", "Desconocido"),
            calories=float(ai_result.get("calories", 0.0)),
            proteins=float(ai_result.get("proteins", 0.0)),
            carbs=float(ai_result.get("carbs", 0.0)),
            fats=float(ai_result.get("fats", 0.0)),
            image_url=uploaded_image_url,
            source=Source.TELEGRAM,
        )

        db.add(food_log_data)
        await db.commit()
        await db.refresh(food_log_data)

        ai_result["log_id"] = str(food_log_data.id)

    except Exception as e:
        await db.rollback()
        print(f"Error guardando FoodLog: {e}")
        raise HTTPException(status_code=500, detail="Error saving FoodLog")

    return ai_result


@router.post("/analyze-web")
async def analyze_food_web(
    file: UploadFile = File(...), current_user=Depends(dependencies.get_current_user)
):

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="No valid image file provided")

    ai_result = await analyze_food_content(
        text_query=None, image_bytes=image_bytes, mime_type=file.content_type
    )

    if not ai_result:
        raise HTTPException(status_code=500, detail="AI could'nt analyze food")

    return ai_result


@router.post("/analyze-text-web")
async def analyze_food_text_web(
    request: TextAnalysisRequest,
    current_user=Depends(dependencies.get_current_user),
):
    ai_result = await analyze_food_content(
        text_query=request.query, image_bytes=None, mime_type=None
    )

    if not ai_result:
        raise HTTPException(
            status_code=500, detail="AI could'nt analyze food with provided text"
        )

    return ai_result
