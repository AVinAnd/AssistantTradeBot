import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import load_config
from handlers import commands

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info('Starting bot')

    config = load_config()
    bot = Bot(token=config('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
