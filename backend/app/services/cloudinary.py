import cloudinary
import cloudinary.uploader
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


async def upload_image_base64(image_base64: str) -> str | None:
    """
    Sube una imagen en formato base64 a Cloudinary y devuelve la URL segura.
    """
    if not image_base64:
        return None

    try:
        data_uri = f"data:image/jpeg;base64,{image_base64}"

        response = cloudinary.uploader.upload(data_uri, folder="snapbite_food_logs")

        return response.get("secure_url")

    except Exception as e:
        print(f"Error subiendo imagen a Cloudinary: {e}")
        return None


async def upload_image(file) -> str | None:
    """
    Sube un archivo binario directamente a Cloudinary.
    """
    try:
        response = cloudinary.uploader.upload(file, folder="snapbite_food_logs")
        return response.get("secure_url")
    except Exception as e:
        print(f"Error subiendo archivo a Cloudinary: {e}")
        return None
