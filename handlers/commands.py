from aiogram import types, Router
from aiogram.filters import Command

from lexicon.lexicon import bot_message

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(bot_message['cmd_start'])


@router.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(bot_message['cmd_help'])
