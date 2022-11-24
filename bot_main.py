import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

load_dotenv()


async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

