import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.config import load_config
from handlers import commands
from services import stock_market

logger = logging.getLogger(__name__)
loop = asyncio.new_event_loop()
scheduler = AsyncIOScheduler(event_loop=loop)


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

    await stock_market.get_shares(logger)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def add_jobs(job_scheduler):
    job_scheduler.add_job(main)
    #job_scheduler.add_job(stock_market.check_prices, 'interval', minutes=10)
    #job_scheduler.add_job(stock_market.test_check, 'interval', seconds=5)
    job_scheduler.start()

if __name__ == '__main__':
    asyncio.run(add_jobs(scheduler))
    loop.run_forever()
