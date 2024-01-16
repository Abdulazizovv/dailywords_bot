from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

refresh_data = CallbackData("refresh", "choice")

refresh_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Refresh🔄", callback_data=refresh_data.new(choice="yes")),
            InlineKeyboardButton(text="Bekor qilish❌", callback_data=refresh_data.new(choice="no"))
        ]
    ]
)