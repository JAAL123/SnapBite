from aiogram import Router, types, F
from aiogram.filters import Command
from app.keyboards import get_main_menu_keyboard
from app.backend_client import get_daily_summary, update_user_goal
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()


class UserSettings(StatesGroup):
    waiting_for_new_goal = State()


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


@router.callback_query(F.data == "adjust_goal")
async def process_adjust_goal_callback(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await callback_query.answer()

    await state.set_state(UserSettings.waiting_for_new_goal)

    await callback_query.message.answer(
        "🎯 Escribe tu nueva meta de calorías diarias (ej. `1800` o `2500`):",
        parse_mode="Markdown",
    )


@router.message(UserSettings.waiting_for_new_goal)
async def process_new_goal_input(message: types.Message, state: FSMContext):

    try:
        new_goal = float(message.text)
        if new_goal < 500 or new_goal > 10000:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Por favor, ingresa un número válido (ej. 2000).")
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    result = await update_user_goal(telegram_id=message.from_user.id, new_goal=new_goal)

    if not result:
        await message.answer("😓 Hubo un error al guardar tu meta. Intenta más tarde.")
    else:
        await message.answer(
            f"✅ ¡Excelente! Tu meta ha sido actualizada a **{new_goal} kcal**.",
            parse_mode="Markdown",
        )
        await state.clear()
