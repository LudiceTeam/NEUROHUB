from aiogram import Bot,Dispatcher,F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,File,Video,PhotoSize
import aiogram
import keyboards as kb

import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) 

sys.path.insert(0, project_root)

router = Router()


@router.message(CommandStart())
async def start_messsage(message:Message):
    await message.answer("Welcome") # вставить сюда норм текст