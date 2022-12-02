from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from app.handlers.callback import BaseCallbackData

# def make_inline_keyboard(items: list[tuple[str, str]]) -> InlineKeyboardMarkup:
#     result_list = []
#     for i in items:
#         result_list.append([InlineKeyboardButton(j[0], callback_data=j[1]) for j in i])
#     return InlineKeyboardMarkup(inline_keyboard=result_list)


def make_inline_column_keyboard(items: list[str]) -> InlineKeyboardMarkup:
    result_list = [[InlineKeyboardButton(text=i, callback_data=items.index(i))] for i in items]
    return InlineKeyboardMarkup(inline_keyboard=result_list)

def make_inline_keyboard(items: list[str], columns:int = 1) -> InlineKeyboardMarkup:
    counter = 1
    temp_list = []
    result_list = []
    for i in items:
        if counter < columns:
            temp_list.append(InlineKeyboardButton(text=i, callback_data=items.index(i)))
            counter += 1
        else:
            temp_list = [InlineKeyboardButton(text=i, callback_data=items.index(i))]
            result_list.append(temp_list.copy())
            counter = 1
    return InlineKeyboardMarkup(inline_keyboard=result_list)

def yes_no_inline_keyboard() -> InlineKeyboardMarkup:
    yes_button = InlineKeyboardButton(text='Да', callback_data='true')
    no_button = InlineKeyboardButton(text='Нет', callback_data='false')
    return InlineKeyboardMarkup(inline_keyboard=[[yes_button, no_button]])