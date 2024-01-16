import asyncio

from aiogram import executor

from bot.handlers.admins.send_word import set_used_false
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import logging

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


async def change_words_status():
    while True:
        await set_used_false()
        print("ishladi")
        await asyncio.sleep(5)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
