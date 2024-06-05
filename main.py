import asyncio, logging, sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from app.handlers import router
from decouple import config


TOKEN = config('TELEGRAM_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')