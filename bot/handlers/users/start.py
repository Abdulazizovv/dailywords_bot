from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.keyboards.default import home
from bot.loader import dp
from botapp.models import TgUser, Words
from asgiref.sync import sync_to_async
import random


@sync_to_async
def add_user(username, first_name, last_name, tg_id):
    if not TgUser.objects.filter(tg_id=tg_id):
        user = TgUser.objects.create(username=username, first_name=first_name,
                            last_name=last_name, tg_id=tg_id)
        return user
    TgUser.objects.update(username=username, first_name=first_name, last_name=last_name)
    return "User exists"


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await add_user(message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.from_user.id)
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=home)


