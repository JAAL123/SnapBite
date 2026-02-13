from google import genai
from app.core.config import settings
import json
import re


client = genai.Client(api_key=settings.GOOGLE_API_KEY)

MODEL_NAME = "gemini-3-flash-preview"

async def analyze_food_content(text_query: str = None):
    """
    Envía texto a Gemini para analizar comida y estimar calorías.
    """
    try:
        prompt = f"""
        You are an expert nutritionist AI. 
        Analyze the following food description: "{text_query}".
        
        Estimate the nutritional values.
        You MUST return the result in raw JSON format (without Markdown code blocks).
        
        The JSON structure must be exactly like this:
        {{
            "food_name": "Short descriptive name",
            "calories": 0.0,
            "proteins": 0.0,
            "carbs": 0.0,
            "fats": 0.0,
            "portion_description": "e.g., 1 medium apple"
        }}
        
        If the input is not food or you can't identify it, return specific fields set to null or 0, but keep the JSON structure.
        """

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        clean_text = response.text
        
        json_match = re.search(r"\{.*\}", clean_text, re.DOTALL)
        if json_match:
            clean_text = json_match.group(0)
            return json.loads(clean_text)
        else:
            return json.loads(clean_text)
            
    except Exception as e:
        print(f"Error calling Gemini ({MODEL_NAME}): {e}")
        return None