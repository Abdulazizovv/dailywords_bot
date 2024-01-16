from aiogram.dispatcher.filters.state import StatesGroup, State


class AddWordState(StatesGroup):
    english_word = State()
    uzbek_word = State()
    variants = State()


class ChangeWordState(StatesGroup):
    word = State()
    english = State()
    uzbek = State()
    v1 = State()
    v2 = State()
    v3 = State()
    v4 = State()
