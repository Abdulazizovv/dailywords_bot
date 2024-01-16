import logging

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

from bot.filters import IsAdmin
from bot.loader import dp
from botapp.models import Words


@sync_to_async
def for_me_please_dont_touch():
    try:
        words = Words.objects.all()
        data = [{"word_count": words.count()}]
        with open("words.txt", "w") as f:
            for word in words:
                data.append(
                    {
                        "english": word.english,
                        "uzbek": word.uzbek,
                        "v1": word.v1,
                        "v2": word.v2,
                        "v3": word.v3,
                        "v4": word.v4,
                        "used": word.used,
                        "created": word.created.strftime('%Y-%m-%d %H:%M:%S %Z'),
                        "updated": word.updated.strftime('%Y-%m-%d %H:%M:%S %Z')
                    }
                )
            f.write(str(data))
    except Exception as err:
        logging.exception(err)
        return False


@sync_to_async
def get_all_words():
    try:
        words = Words.objects.all().order_by("-updated")
        with open("all_words.txt", "w") as f:
            f.write("Word Count: {}\n".format(words.count()))
            for idx, word in enumerate(words, start=1):
                f.write("{})English: {}\n".format(idx, word.english))
                f.write("Uzbek: {}\n".format(word.uzbek))
                f.write("V1: {}\n".format(word.v1))
                f.write("V2: {}\n".format(word.v2))
                if word.v3 is not None:
                    f.write("V3: {}\n".format(word.v3))
                if word.v4 is not None:
                    f.write("V4: {}\n".format(word.v4))
                f.write("Used: {}\n".format(word.used))
                f.write("Created: {}\n".format(word.created.strftime('%Y-%m-%d %H:%M:%S %Z')))
                f.write("Updated: {}\n".format(word.updated.strftime('%Y-%m-%d %H:%M:%S %Z')))
                f.write("\n")
        return True
    except Exception as err:
        logging.exception(err)
        return False


@sync_to_async
def get_info():
    words_count = Words.objects.all().count()
    sent_word = Words.objects.filter(used=True).count()
    text = (f"=======Info=======\n"
            f"Jami: {words_count} so'z\n"
            f"Yuborilgan: {sent_word} so'z\n"
            f"Qoldi: {words_count - sent_word} ta\n"
            f"==================")
    return text


@dp.message_handler(IsAdmin(), text="Infoℹ️", state="*")
async def info(message: types.Message):
    await get_all_words()
    text = await get_info()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Faylni yuklash", callback_data="get_file")
            ]
        ]
    )
    await message.answer(text, reply_markup=kb)


@dp.callback_query_handler(text="get_file")
async def send_file(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await get_all_words()
    with open("all_words.txt", "rb") as f:
        await call.message.answer_document(f, caption="Barcha so'zlar")
