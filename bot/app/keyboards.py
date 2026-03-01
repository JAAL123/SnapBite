from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Genera el teclado interactivo para el menú principal.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Mi Resumen de Hoy", callback_data="summary_today"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎯 Ajustar Meta de Calorías", callback_data="adjust_goal"
                )
            ],
        ]
    )
    return keyboard
