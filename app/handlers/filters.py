from aiogram.filters import Filter
from aiogram.types import Message


class ContactFilter(Filter):
    def __init__(self):
        pass
    async def __call__(self, message: Message) -> bool:
        return message.contact != None