import base64
from fastapi import APIRouter, HTTPException
from app.services.gemini import analyze_food_content
from pydantic import BaseModel

router = APIRouter()

class AnalysisRequest(BaseModel):
    query: str | None = None          
    image_base64: str | None = None   
    media_type: str = "image/jpeg"     

@router.post("/analyze")
async def analyze_food(request: AnalysisRequest):
    """
    Analiza comida (texto y/o imagen) y devuelve JSON nutricional.
    """
    image_bytes = None
    
    if request.image_base64:
        try:
            image_bytes = base64.b64decode(request.image_base64)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")

    if not request.query and not image_bytes:
        raise HTTPException(status_code=400, detail="Provide text query or image")

    result = await analyze_food_content(
        text_query=request.query, 
        image_bytes=image_bytes, 
        mime_type=request.media_type
    )
    
    if not result:
        raise HTTPException(status_code=500, detail="Could not analyze food with AI")
        
    return result