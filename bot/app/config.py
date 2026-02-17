import os
from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000/api/v1")

if not TELEGRAM_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN provided")