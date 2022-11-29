from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_keyboard_column(items: list[str]) -> ReplyKeyboardMarkup:
    column = [[KeyboardButton(text=item)] for item in items]
    return ReplyKeyboardMarkup(keyboard=column, resize_keyboard=True)

def phone_request_keyboard():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Поделиться номером телефона',request_contact=True)], [KeyboardButton(text='Пропустить')]], resize_keyboard=True)