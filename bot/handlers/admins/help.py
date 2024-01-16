from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from bot.filters import IsAdmin
from bot.loader import dp


@dp.message_handler(IsAdmin(), CommandHelp(), state="*")
async def help(message: types.Message):
    text = (f"Qo'llanma:\n"
            f"/start - botni qayta ishga tushurish\n"
            f"/help - yordam bo'limi\n\n"
            f"/add_word - yangi so'z qo'shish\n"
            f"/edit_word - so'zni o'zgartirish\n\n"
            f"/start_question - so'z yuborishni boshlash\n"
            f"/stop_question - so'z yuborishni to'xtatish\n"
            f"/set_time n -  so'z yuborish vaqtini n ga o'zgartirish(default 3600)")
    await message.answer(text)
