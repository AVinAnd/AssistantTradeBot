from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

async def say_hi():
    await asyncio.sleep(2)
    print('hi')

loop = asyncio.new_event_loop()
scheduler = AsyncIOScheduler(event_loop=loop)
scheduler.add_job(say_hi, 'interval', seconds=5)
scheduler.start()
loop.run_forever()
