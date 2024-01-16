import asyncio

from aiogram import executor
from django.core.management.base import BaseCommand
import logging

from bot import filters
from bot import middlewares, handlers
from bot.handlers.admins.send_word import set_used_false

from bot.loader import dp
from bot.utils.notify_admins import on_startup_notify
from bot.utils.set_bot_commands import set_default_commands


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        pass


logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    filters.setup(dp)
    middlewares.setup(dp)
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


async def change_words_status():
    while True:
        await set_used_false()
        await asyncio.sleep(3600)


loop = asyncio.get_event_loop()
loop.create_task(change_words_status())
executor.start_polling(dp, on_startup=on_startup, skip_updates=True, fast=True)
