import asyncio
from aiogram import Bot, Dispatcher, types

from config import config
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(bot=bot)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer('Hello!')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())