import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from app.config import TELEGRAM_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"¡Hola {user_name}! 👋\nSoy SnapBite Bot 🍎.\n\nEstoy listo para ayudarte a contar calorías usando IA."
    )


@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(
        "Aún no sé qué hacer con esto, pero pronto podré analizar tu comida 📸."
    )


async def main():
    print("🚀 Bot iniciado...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot detenido")
