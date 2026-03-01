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


def get_undo_keyboard(log_id: str) -> InlineKeyboardMarkup:
    """
    Genera un botón para deshacer/borrar un registro de comida recién creado.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Deshacer (Borrar registro)", callback_data=f"undo_{log_id}"
                )
            ]
        ]
    )
    return keyboard
