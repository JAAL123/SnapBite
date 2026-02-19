import aiohttp
from app.config import BACKEND_URL

async def analyze_text_with_backend(text: str | None = None, image_base64: str | None = None):
    """
    Envía texto y/o imagen en Base64 al endpoint /ai/analyze del backend.
    """
    url = f"{BACKEND_URL}/ai/analyze"
    
    payload = {}
    if text:
        payload["query"] = text
    if image_base64:
        payload["image_base64"] = image_base64
        payload["media_type"] = "image/jpeg"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    print(f"❌ Error del Backend ({response.status}): {error_text}")
                    return None
    except Exception as e:
        print(f"🔥 Error de conexión con el Backend: {e}")
        return None