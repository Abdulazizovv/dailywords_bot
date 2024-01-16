from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("add_word", "Yangi so'z qo'shish"),
            types.BotCommand("edit_word", "So'zni tahrirlash"),
            types.BotCommand("start_question", "So'z yuborishni boshlash"),
            types.BotCommand("stop_question", "So'z yuborishni to'xtatish"),
            types.BotCommand("set_time", "So'z yuborish vaqtini sozlash")
        ]
    )
