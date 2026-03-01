from aiogram import Router, types, F
from aiogram.filters import Command
from app.keyboards import get_main_menu_keyboard
from app.backend_client import get_daily_summary

router = Router()


@router.message(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer(
        "¿Qué te gustaría hacer? Elige una opción:",
        reply_markup=get_main_menu_keyboard(),
    )


@router.callback_query(F.data == "summary_today")
async def process_summary_callback(callback_query: types.CallbackQuery):

    await callback_query.answer()

    await callback_query.bot.send_chat_action(
        chat_id=callback_query.message.chat.id, action="typing"
    )

    summary = await get_daily_summary(callback_query.from_user.id)

    if not summary:
        await callback_query.message.answer(
            "📝 *Aún no tienes registros de comida.*\n\n"
            "¡Envíame una foto de lo que estés comiendo o descríbelo en texto para crear tu perfil y empezar tu conteo de hoy!",
            parse_mode="Markdown",
        )
        return

    macros = summary.get("macros", {})
    
    text = (
        f"📊 *Tu Resumen de Hoy*\n\n"
        f"🎯 *Meta Diaria:* {summary.get('daily_goal')} kcal\n"
        f"🔥 *Consumido:* {summary.get('consumed_calories')} kcal\n"
        f"📉 *Restante:* {summary.get('remaining_calories')} kcal\n\n"
        f"*Distribución de Macros:*\n"
        f"💪 Proteínas: {macros.get('proteins')}g\n"
        f"🍞 Carbos: {macros.get('carbs')}g\n"
        f"🥑 Grasas: {macros.get('fats')}g"
    )

    await callback_query.message.answer(text, parse_mode="Markdown")
