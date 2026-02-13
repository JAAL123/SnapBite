from fastapi import APIRouter, HTTPException, Body
from app.services.gemini import analyze_food_content
from pydantic import BaseModel

router = APIRouter()

class AnalysisRequest(BaseModel):
    query: str

@router.post("/analyze")
async def analyze_food(request: AnalysisRequest):
    result = await analyze_food_content(request.query)
    
    if not result:
        raise HTTPException(status_code=500, detail="Could not analyze food with AI")
        
    return result