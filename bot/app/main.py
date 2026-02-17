import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from app.config import TELEGRAM_TOKEN
from app.backend_client import analyze_text_with_backend


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "¡Hola! 👋 Soy SnapBite Bot 🍎.\n\n"
        "Escríbeme qué comiste (ej: '2 huevos con jamón') y te diré sus calorías."
    )


@dp.message()
async def handle_food_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    user_text = message.text
    
    data = await analyze_text_with_backend(user_text)
    
    if not data:
        await message.answer("😓 Ups, tuve un problema conectando con mi cerebro. Intenta de nuevo más tarde.")
        return

    response_text = (
        f"🍎 *{data.get('food_name', 'Comida')}*\n"
        f"_{data.get('portion_description', '')}_\n\n"
        f"🔥 *Calorías:* {data.get('calories')} kcal\n"
        f"💪 *Proteínas:* {data.get('proteins')}g\n"
        f"🍞 *Carbos:* {data.get('carbs')}g\n"
        f"🥑 *Grasas:* {data.get('fats')}g"
    )

    await message.answer(response_text, parse_mode="Markdown")

async def main():
    print("🚀 Bot iniciado y escuchando...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot detenido")