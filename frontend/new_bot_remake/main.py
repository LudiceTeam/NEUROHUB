import aiogram
from dotenv import load_dotenv
import os
from aiogram import Bot,Dispatcher
import asyncio
from handlers import router
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) 

sys.path.insert(0, project_root)

load_dotenv()

bot = Bot(os.getenv("BOT"))
dp = Dispatcher()



async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("DONE")