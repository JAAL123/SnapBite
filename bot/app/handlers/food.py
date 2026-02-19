import base64
from aiogram import Router, types, F, Bot
from app.backend_client import analyze_text_with_backend

router = Router()

@router.message(F.photo)
async def handle_food_image(message: types.Message, bot: Bot):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    photo = message.photo[-1]
    
    file_info = await bot.get_file(photo.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    
    image_bytes = downloaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    user_text = message.caption
    
    data = await analyze_text_with_backend(text=user_text, image_base64=image_base64)
    
    if not data:
        await message.answer("😓 Ups, tuve un problema procesando la imagen. Intenta de nuevo más tarde.")
        return

    response_text = (
        f"📸 *{data.get('food_name', 'Comida')}*\n"
        f"_{data.get('portion_description', '')}_\n\n"
        f"🔥 *Calorías:* {data.get('calories')} kcal\n"
        f"💪 *Proteínas:* {data.get('proteins')}g\n"
        f"🍞 *Carbos:* {data.get('carbs')}g\n"
        f"🥑 *Grasas:* {data.get('fats')}g"
    )

    await message.answer(response_text, parse_mode="Markdown")


@router.message(F.text)
async def handle_food_text(message: types.Message, bot: Bot):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    data = await analyze_text_with_backend(text=message.text)
    
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