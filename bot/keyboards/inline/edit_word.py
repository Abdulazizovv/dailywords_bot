from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

edit_word_data = CallbackData("edit", "part")

edit_word_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="english", callback_data=edit_word_data.new(part="english")),
            InlineKeyboardButton(text="uzbek", callback_data=edit_word_data.new(part="uzbek"))
        ],
        [
            InlineKeyboardButton(text="variant 1", callback_data=edit_word_data.new(part="v1")),
            InlineKeyboardButton(text="variant 2", callback_data=edit_word_data.new(part="v2"))
        ],
        [
            InlineKeyboardButton(text="variant 3", callback_data=edit_word_data.new(part="v3")),
            InlineKeyboardButton(text="variant 4", callback_data=edit_word_data.new(part="v4"))
        ],
        [
            InlineKeyboardButton(text="Change used", callback_data=edit_word_data.new(part="used"))
        ],
        [
            InlineKeyboardButton(text="Submit", callback_data=edit_word_data.new(part="submit"))
        ]
    ]
)