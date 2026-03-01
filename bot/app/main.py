import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from app.config import TELEGRAM_TOKEN

from app.handlers.base import router as base_router
from app.handlers.food import router as food_router
from app.handlers.menu import router as menu_router

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    dp.include_router(base_router)
    dp.include_router(menu_router)
    dp.include_router(food_router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Iniciar o reiniciar el bot"),
        BotCommand(command="menu", description="Ver mi resumen diario"),
        BotCommand(command="cancelar", description="Cancelar acción actual")
    ])

    print("🚀 Bot iniciado")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot detenido")