from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.keyboards.default import home
from bot.loader import dp
from botapp.models import TgUser, Words
from asgiref.sync import sync_to_async
import random
from bot.filters.is_admin import IsAdmin
from bot.data.config import CHANNEL_ID


# @sync_to_async
# def add_user(username, first_name, last_name, tg_id):
#     if not TgUser.objects.filter(tg_id=tg_id):
#         user = TgUser.objects.create(username=username, first_name=first_name,
#                             last_name=last_name, tg_id=tg_id)
#         return user
#     TgUser.objects.update(username=username, first_name=first_name, last_name=last_name)
#     return False
#
#
# @sync_to_async
# def random_word():
#     words = list(Words.objects.order_by('?').all()[:4])
#     lang = random.choice(['uzbek', 'english'])
#     word = random.choice(words)
#     options = [getattr(i, lang) for i in words]
#     correct_option = ''
#     if lang == 'uzbek':
#         correct_option = word.uzbek
#         lang = 'english'
#     elif lang == 'english':
#         correct_option = word.english
#         lang = 'uzbek'
#     return word, lang, options, correct_option
#
#
# async def create_poll():
#     data = await random_word()
#     print(data)
#     question = f'{getattr(data[0], data[1])} in {data[1]}?'
#     correct_answer = data[2].index(data[3])
#     explain = 'Ok'
#     options = data[2]
#     try:
#         poll = await dp.bot.send_poll(
#                 CHANNEL_ID,
#                 question,
#                 options=options,
#                 type=types.PollType.QUIZ,  # Set poll type to QUIZ
#                 correct_option_id=correct_answer,  # Index of the correct answer in the options list
#                 is_anonymous=True,
#                 explanation=explain,  # Explanation for the correct answer
#                 explanation_parse_mode=types.ParseMode.MARKDOWN
#             )
#     except Exception as err:
#         print(err)


@dp.message_handler(CommandStart(), IsAdmin())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}\n", reply_markup=home)