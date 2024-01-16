from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

call_data = CallbackData("submit", "yes")

kb_submit = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Tasdiqlash✅", callback_data=call_data.new(yes="yes")),
            InlineKeyboardButton(text="Bekor qilish❌", callback_data=call_data.new(yes='no'))
        ]
    ]
)
