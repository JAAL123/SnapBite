from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    query: str = Field(
        ..., min_length=1, description="Description of the food or drink to analyze"
    )


class AIAnalysisResponse(BaseModel):
    food_name: str
    calories: float
    proteins: float
    carbs: float
    fats: float
