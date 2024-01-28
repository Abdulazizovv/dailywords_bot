from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async
from django.db.models import Q
import json
import random
from bot.keyboards.default import home
from bot.keyboards.inline import kb_submit, refresh_kb, refresh_data
from bot.keyboards.inline.submit_word_kb import call_data
from bot.states.word_state import AddWordState
from bot.loader import dp
from botapp.models import Words
from bot.filters.is_admin import IsAdmin


async def get_suggestion():
    with open("words.json", "r") as f:
        data = json.loads(f.read())
        random_words = [random.choice(data) for i in range(5)]
        return random_words


@sync_to_async
def check_word(english):
    if Words.objects.filter(english__icontains=english):
        return False
    return True


@dp.message_handler(text='Bekor qilish❌', state="*")
async def cancel_word(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Bekor qilindi!", reply_markup=home)


@dp.message_handler(IsAdmin(), Command("add_word"), state="*")
@dp.message_handler(IsAdmin(), text="Yangi so'z qo'shish🆕", state="*")
async def add_word(message: types.Message, state: FSMContext):
    kb_cancel = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("Bekor qilish❌")
            ]
        ],
        resize_keyboard=True
    )
    suggestion_words = await get_suggestion()
    text = ''
    for k, i in enumerate(suggestion_words):
        text += f"{k+1}) {i['english']} - {i['uzbek']}\n"
    await message.answer(f"Marhamat inglizcha so'z yuboring.\n"
                         f"Pastda esa tavsiyalar\n\n"
                         f"{text}", reply_markup=refresh_kb)
    await AddWordState.english_word.set()


@dp.callback_query_handler(refresh_data.filter(), state="*")
async def refresh_suggest(call: types.CallbackQuery, state: FSMContext):

    if call.data[8:] == "yes":
        words = await get_suggestion()
        text = ''
        for k, i in enumerate(words):
            text += f"{k+1}) {i['english']} - {i['uzbek']}\n"
        await call.message.edit_text(f"Marhamat inglizcha so'z yuboring.\n"
                                     f"Pastda esa tavsiyalar\n\n"
                                     f"{text}", reply_markup=refresh_kb)
    elif call.data[8:] == "no":
        await call.message.delete()
        await dp.bot.send_message(chat_id=call.message.chat.id, text="Bekor qilindi!", reply_markup=home)


@dp.message_handler(content_types=['text'], state=AddWordState.english_word)
async def get_english_word(message: types.Message, state: FSMContext):
    english = message.text
    if await check_word(english):
        await state.update_data(english=message.text.lower())
        await message.answer(f"<b>{message.text}</b> qabul qilindi. Endi o'zbekcha tarjimasini yuboring")
        await AddWordState.uzbek_word.set()
    else:
        await message.answer("Siz kiritmoqchi bo'lgan so'z bazada mavjud")


@dp.message_handler(content_types=['text'], state=AddWordState.uzbek_word)
async def get_uzbek_word(message: types.Message, state: FSMContext):
    await state.update_data(uzbek=message.text.lower())
    data = await state.get_data()
    await message.answer(f"{data.get('english')} - {data.get('uzbek')}\n"
                         f"So'z qabul qilindi. Variantlarni quyidagi ko'rinishda yuboring:\n\n"
                         f"<code>variant1, variant2, variant3, variant4 </code>\n\n"
                         f"<b>Eslatma:</b>\n"
                         f"<i>To'g'ri javobni yubormang!\nHar bir variantdan so'ng vergul(,) belgisini qo'ying. Vargul belgisigacha bo'lgan barcha so'zlar bitta "
                         f"variant sifatida olinadi. Variantlar ko'pi bilan 4 ta, eng kamida 2 bo'lishi lozim</i>")
    await AddWordState.variants.set()


@dp.message_handler(state=AddWordState.variants)
async def get_variants(message: types.Message, state: FSMContext):
    variants = message.text.lower().strip().split(",")
    variants_text = ''
    await state.update_data(variants=variants)
    data = await state.get_data()
    print(type(data.get("variants")))
    if len(variants) >= 2 <= 4:
        for k, i in enumerate(variants):
            variants_text += f"variant_{k+1}: <b>{i.strip()}</b>\n"
        await message.answer(f"<b>So'z: {data.get('english')} 👉 {data.get('uzbek')}</b>\n"
                             f"<i>variantlar:</i>\n\n"
                             f"<code>{variants_text}</code>\n\n"
                             f"<i>Barchasi to'gri ekanligini tasdiqlang</i>", reply_markup=kb_submit)


@sync_to_async
def add_word(english, uzbek, variants):
    if not Words.objects.filter(Q(english=english)):
        word = Words.objects.create(english=english, uzbek=uzbek)
        if len(variants) == 2:
            word.v1 = variants[0]
            word.v2 = variants[1]
        elif len(variants) == 3:
            word.v1 = variants[0]
            word.v2 = variants[1]
            word.v3 = variants[2]
        elif len(variants) == 4:
            word.v1 = variants[0]
            word.v2 = variants[1]
            word.v3 = variants[2]
            word.v4 = variants[3]
        word.save()
        return word
    return False


@dp.callback_query_handler(call_data.filter(), state="*")
async def submit_word(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data)
    if call.data[7:] == "yes":
        if await add_word(data.get("english"), data.get("uzbek"), data.get("variants")):
            await call.message.delete()
            await dp.bot.send_message(chat_id=call.message.chat.id, text="So'z muvaffaqqiyatli qo'shildi✅", reply_markup=home)
            await state.reset_state()
        else:
            await call.message.edit_text("Siz kiritmoqchi bo'lgan so'z mavjud")
    else:
        await call.message.delete()
        await call.message.answer("Bekor qilindi", reply_markup=home)
        await state.finish()
