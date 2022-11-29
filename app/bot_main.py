import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import handlers.bot_start_route

load_dotenv()

dp: Dispatcher = Dispatcher()
bot: Bot = Bot(token=os.getenv('BOT_TOKEN'))


async def main():
    global bot
    global dp
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(handlers.bot_start_route.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

