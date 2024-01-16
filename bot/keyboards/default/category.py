from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

home = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Yangi so'z qo'shish🆕"),
            KeyboardButton("So'zni tahrirlash✏️")
        ],
        [
            KeyboardButton("So'z yuborishni boshlash▶️")
        ],
        [
            KeyboardButton("1️⃣ ta so'z yuborish")
        ],
        [
            KeyboardButton("Infoℹ️")
        ]
    ],
    resize_keyboard=True
)
