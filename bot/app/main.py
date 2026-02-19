import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.config import TELEGRAM_TOKEN

from app.handlers.base import router as base_router
from app.handlers.food import router as food_router

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    dp.include_router(base_router)
    dp.include_router(food_router)

    print("🚀 Bot iniciado (arquitectura modular)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot detenido")