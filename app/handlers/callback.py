from aiogram.filters.callback_data import CallbackData

class StatusCallbackData(CallbackData, prefix = 'status'):
    text: str

class BaseCallbackData(CallbackData, prefix='base'):
    text: str

