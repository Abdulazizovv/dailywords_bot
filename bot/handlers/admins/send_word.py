import logging
import random
from datetime import datetime, timezone, timedelta

from aiogram import types
from aiogram.dispatcher.filters import Command
from asgiref.sync import sync_to_async

from bot.data.config import CHANNEL_ID, ADMINS
from bot.filters import IsAdmin
from bot.loader import dp, scheduler
from botapp.models import Words


# get 1 random not sent word from database
@sync_to_async
def get_word():
    words = Words.objects.filter(used=False)
    if words:
        word = random.choice(list(words))
        word.used = True
        word.save()
        return word
    return False


async def send_poll():
    word = await get_word()
    if word:
        question = f"{word.english} means?"
        options1 = [getattr(word, f"v{i}") for i in range(1, 5) if hasattr(word, f"v{i}") and getattr(word, f"v{i}") is not None]
        options =[]
        for i in options1:
            options.append(i.strip())
        options.append(word.uzbek)
        options = random.sample(options, len(options))
        correct_answer = options.index(word.uzbek)
        explain = f"{word.english} - {word.uzbek}"
        await dp.bot.send_poll(
            CHANNEL_ID,
            question,
            options=options,
            type=types.PollType.QUIZ,  # Set poll type to QUIZ
            correct_option_id=correct_answer,  # Index of the correct answer in the options list
            is_anonymous=True,
            explanation=explain,  # Explanation for the correct answer
            explanation_parse_mode=types.ParseMode.MARKDOWN
        )
        return True
    else:
        for admin in ADMINS:
            try:
                await dp.bot.send_message(chat_id=admin, text="So'z yuborish to'xtatildi. Sabab bazada yuborilmagan so'z qolmadi!")
            except Exception as err:
                logging.exception(err)
        if scheduler.running:
            scheduler.shutdown()
        return False


@dp.message_handler(IsAdmin(), Command("start_question"), state="*")
@dp.message_handler(text="So'z yuborishni boshlash▶️", state="*")
async def start_send_word(message: types.Message):
    await set_used_false()
    with open("time.txt") as file:
        time = int(file.read().strip())
    if not time or time < 0 or time <= 10:
        time = 3600
        await message.answer("So'z yuborish oralig'i no'to'gri kiritildi.\n"
                             f"Shuning uchun avtomatik {time} sekundga o'zgartirildi!")
    print(time)
    scheduler.add_job(send_poll, trigger='interval', seconds=time)
    if not scheduler.running:
        scheduler.start()
        for i in scheduler.get_jobs():
            await message.answer(
                f"So'zlarni yuborish boshlandi.\nTo'xtatish uchun /stop_question \nKeyingisi : {i.next_run_time.strftime('%H:%M:%S %d-%m-%Y')}")
    else:
        for i in scheduler.get_jobs():
            await message.answer("So'zlarni yuborish boshlangan.\n"
                                 f"Keyingisi: {i.next_run_time.strftime('%H:%M:%S %d-%m-%Y')}"
                                 "To'xtatish uchun /stop_question")


@dp.message_handler(Command("set_time"), IsAdmin(), state="*")
async def set_time(message: types.Message):
    if len(message.text.split()) == 2:
        if message.text.split()[1].isdigit():
            time = message.text.split()[1]
            with open("time.txt", "w") as file:
                file.write(time)
            await message.answer(f"Test yuborish intervali yangilandi! {time} sekund")
    else:
        await message.reply("/set_time buyrug'idan keyin sekundlar miqdorini kiriting\n"
                            "Masalan:\n"
                            "<i> /set_time 360 </i>")


@dp.message_handler(IsAdmin(), Command("stop_question"), state="*")
async def stop_question(message: types.Message):
    try:
        scheduler.shutdown()
        await message.answer("So'z yuborish to'xtatildi. Boshlash uchun /start_question")
    except Exception as err:
        print(err)
        await message.answer("So'z yuborish hali boshlanmadi!")


@dp.message_handler(IsAdmin(), text="1️⃣ ta so'z yuborish")
async def send_one_word(message: types.Message):
    if await send_poll():
        await message.reply("1 ta so'z yuborildi!")


# automatically sent words status change to not sent script
# this script automatically run always
@sync_to_async
def set_used_false():
    used_words = Words.objects.filter(used=True)
    for word in used_words:
        # Make word.updated UTC-aware if it's not already
        if word.updated.tzinfo is None or word.updated.tzinfo.utcoffset(word.updated) is None:
            word.updated = word.updated.replace(tzinfo=timezone.utc)

        delta = datetime.utcnow().replace(tzinfo=timezone.utc) - word.updated
        if delta >= timedelta(days=2):
            word.used = False
            word.save()
    print("ishladi")