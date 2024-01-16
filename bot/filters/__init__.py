from aiogram import Dispatcher

from bot.loader import dp
from .is_admin import IsAdmin



def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    pass

if __name__ == "filters":
    # dp.filters_factory.bind(IsAdmin)
    pass
