from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from app.handlers.callback import BaseCallbackData

# def make_inline_keyboard(items: list[tuple[str, str]]) -> InlineKeyboardMarkup:
#     result_list = []
#     for i in items:
#         result_list.append([InlineKeyboardButton(j[0], callback_data=j[1]) for j in i])
#     return InlineKeyboardMarkup(inline_keyboard=result_list)


def make_inline_column_keyboard(items: list[str], Callback_type:BaseCallbackData = BaseCallbackData) -> InlineKeyboardMarkup:
    result_list = [[InlineKeyboardButton(text=i, callback_data=Callback_type(text=i).pack())] for i in items]
    return InlineKeyboardMarkup(inline_keyboard=result_list)
