from aiogram import Router, types
from aiogram.filters import CommandStart

# Creamos el router para este módulo
router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "¡Hola! 👋 Soy SnapBite Bot 🍎.\n\n"
        "Escríbeme qué comiste o **envíame una foto de tu plato** y te diré sus calorías."
    )