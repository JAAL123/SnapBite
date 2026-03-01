from aiogram import Router, types
from aiogram.filters import CommandStart, Command

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "¡Hola! 👋 Soy **SnapBite Bot** 🍎.\n\n"
        "Llevar tu conteo de calorías nunca fue tan fácil.\n "
        "🍽️ **¿Cómo registrar comida?**\n"
        "Simplemente **escríbeme** (ej. 'dos huevos y un pan') o **envíame una foto** de tu plato en cualquier momento.\n\n"
        "📊 **¿Cómo ver mi progreso?**\n"
        "Usa el comando /menu o búscalo en el botón de la esquina inferior izquierda.",
        parse_mode="Markdown",
    )


@router.message(Command("cancelar"))
async def cmd_cancel(message: types.Message):
    await message.answer(
        "✅ Acción cancelada. Puedes seguir registrando comidas enviándome texto o fotos.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
