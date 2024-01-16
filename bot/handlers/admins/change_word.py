from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from asgiref.sync import sync_to_async
from django.db.models import Q
from bot.filters import IsAdmin
from bot.keyboards.inline import edit_word_kb, edit_word_data
from bot.loader import dp
from bot.states.word_state import ChangeWordState
from botapp.models import Words


@sync_to_async
def get_word(term):
    word = Words.objects.filter(Q(english__iexact=term) | Q(uzbek__iexact=term)).first()
    return word


@sync_to_async
def change_used(word):
    if word.used:
        word.used = False
    else:
        word.used = True
    word.save()


@dp.message_handler(IsAdmin(), Command("edit_word"), state="*")
@dp.message_handler(IsAdmin(), text="So'zni tahrirlash✏️", state="*")
async def change_word(message: types.Message, state: FSMContext):
    await message.answer("Marhamat o'zgartirmoqchi bo'lgan so'zingizni yuboring")
    await ChangeWordState.word.set()


@dp.message_handler(state=ChangeWordState.word)
async def get_change_word(message: types.Message, state: FSMContext):
    word = await get_word(message.text)
    await state.update_data(word=word)
    variants_text = ''
    if word:
        await message.answer(f"So'z topildi!\n"
                             f"{word.english} - {word.uzbek}\n"
                             f"variant 1: {word.v1}\n"
                             f"variant 2: {word.v2}\n"
                             f"variant 3: {word.v3}\n"
                             f"variant 4: {word.v4}\n"
                             f"used: {word.used}", reply_markup=edit_word_kb)
    else:
        await message.answer("Siz qidirgan so'z topilmadi!\n"
                             "Qaytadan urinib ko'ring")


@dp.callback_query_handler(edit_word_data.filter(), state="*")
async def edit_word(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    word = data.get("word")
    if call.data[5:] == 'english':
        await call.message.delete()
        await call.message.answer("Marhamat so'zni yuboring")
        await ChangeWordState.english.set()
    elif call.data[5:] == 'uzbek':
        await call.message.delete()
        await call.message.answer("Marhamat so'zni yuboring")
        await ChangeWordState.uzbek.set()
    elif call.data[5:] == 'used':
        await change_used(word=word)
        await call.message.edit_text(f"{word.english} - {word.uzbek}\n"
                                     f"used: {word.used}\n"
                                     f"So'z o'zgartirildi")
    elif call.data[5:] == 'v1':
        await call.message.edit_text("1-variant uchun yangi matn kiriting...")
        await ChangeWordState.v1.set()
    elif call.data[5:] == 'v2':
        await call.message.edit_text("2-variant uchun yangi matn kiriting...")
        await ChangeWordState.v2.set()
    elif call.data[5:] == 'v3':
        await call.message.edit_text("3-variant uchun yangi matn kiriting...")
        await ChangeWordState.v3.set()
    elif call.data[5:] == 'v4':
        await call.message.edit_text("4-variant uchun yangi matn kiriting...")
        await ChangeWordState.v4.set()
    else:
        await state.finish()
        await call.message.edit_text("Barcha o'zgarishlar saqlandi!")


@sync_to_async
def change_v1(word, text):
    word.v1 = text
    word.save()


@dp.message_handler(state=ChangeWordState.v1)
async def get_v1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    word = data.get("word")
    text = message.text
    await change_v1(word, text)
    await message.answer(f"So'z o'zgartirildi!\n"
                         f"{word.english} - {word.uzbek}\n\n"
                         f"<code>variant 1: {word.v1}\n"
                         f"variant 2: {word.v2}\n"
                         f"variant 3: {word.v3}\n"
                         f"variant 4: {word.v4}</code>\n\n"
                         f"used: {word.used}", reply_markup=edit_word_kb)


@sync_to_async
def change_v2(word, text):
    word.v2 = text
    word.save()


@dp.message_handler(state=ChangeWordState.v2)
async def get_v2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    word = data.get("word")
    text = message.text
    await change_v2(word, text)
    await message.answer(f"So'z o'zgartirildi!\n"
                         f"{word.english} - {word.uzbek}\n\n"
                         f"<code>variant 1: {word.v1}\n"
                         f"variant 2: {word.v2}\n"
                         f"variant 3: {word.v3}\n"
                         f"variant 4: {word.v4}</code>\n\n"
                         f"used: {word.used}", reply_markup=edit_word_kb)


@sync_to_async
def change_v3(word, text):
    word.v3 = text
    word.save()


@dp.message_handler(state=ChangeWordState.v3)
async def get_v1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    word = data.get("word")
    text = message.text
    await change_v3(word, text)
    await message.answer(f"So'z o'zgartirildi!\n"
                         f"{word.english} - {word.uzbek}\n\n"
                         f"<code>variant 1: {word.v1}\n"
                         f"variant 2: {word.v2}\n"
                         f"variant 3: {word.v3}\n"
                         f"variant 4: {word.v4}</code>\n\n"
                         f"used: {word.used}", reply_markup=edit_word_kb)


@sync_to_async
def change_v4(word, text):
    word.v4 = text
    word.save()


@dp.message_handler(state=ChangeWordState.v4)
async def get_v1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    word = data.get("word")
    text = message.text
    await change_v4(word, text)
    await message.answer(f"So'z o'zgartirildi!\n"
                         f"{word.english} - {word.uzbek}\n\n"
                         f"<code>variant 1: {word.v1}\n"
                         f"variant 2: {word.v2}\n"
                         f"variant 3: {word.v3}\n"
                         f"variant 4: {word.v4}</code>\n\n"
                         f"used: {word.used}", reply_markup=edit_word_kb)


@sync_to_async
def change_english(word, english: str):
    word.english = english
    word.save()


@sync_to_async
def change_uzbek(word, uzbek: str):
    word.uzbek = uzbek
    word.save()


@dp.message_handler(state=ChangeWordState.english)
async def get_english(message: types.Message, state: FSMContext):
    data = await state.get_data()
    word = data.get("word")
    await change_english(word, english=message.text)
    await message.answer("So'z o'zgartirildi\n"
                         f"{word.english} - {word.uzbek}\n"
                         f"used: {word.used}", reply_markup=edit_word_kb)


@dp.message_handler(state=ChangeWordState.uzbek)
async def get_uzbek(message: types.Message, state: FSMContext):
    data = await state.get_data()
    word = data.get("word")
    await change_uzbek(word, uzbek=message.text)
    await message.answer("So'z o'zgartirildi\n"
                         f"{word.english} - {word.uzbek}\n"
                         f"used: {word.used}", reply_markup=edit_word_kb)
