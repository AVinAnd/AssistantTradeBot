import asyncio

from aiogram import Bot
from tinkoff.invest import AsyncClient, Client

from config.config import load_config
from lexicon.lexicon import generate_price_changing_text

shares = {}
config = load_config()
tinkoff_client = Client(config('TINKOFF_TOKEN'))
bot = Bot(token=config('BOT_TOKEN'))


async def get_shares():
    with tinkoff_client as client:
        account = client.users.get_accounts().accounts[1]
        account_positions = client.operations.get_portfolio(
            account_id=account.id
        ).positions
        uid_list = [account_positions[i].instrument_uid
                    for i in range(len(account_positions))]

        for uid in uid_list:
            active = client.instruments.find_instrument(query=uid)
            if active.instruments:
                shares[uid] = {'name': active.instruments[0].name}

        current_prices = await get_shares_prices()
        for uid in current_prices.keys():
            shares[uid]['starting_price'] = current_prices[uid]
        print(shares)

        #logger.info(shares)


async def get_shares_prices() -> dict:
    current_prices = {}
    with tinkoff_client as client:
        prices = client.market_data.get_last_prices(
            instrument_id=[*shares.keys()]
        ).last_prices
        for i in range(len(shares)):
            uid = prices[i].instrument_uid
            price_unit = prices[i].price.units
            price_nano = prices[i].price.nano // 10000000
            share_price = float(f'{price_unit}.{price_nano}')
            current_prices[uid] = share_price
        return current_prices


async def check_prices():
    current_prices = await get_shares_prices()
    for uid in [*shares.keys()]:
        price_change = current_prices[uid] / shares[uid]['starting_price']
        if not 0.95 < price_change < 1.05:
            text = await generate_price_changing_text(shares[uid]['name'])
            await bot.send_message(chat_id=config('TG_ID'), text=text)


async def test_check():
    current_prices = await get_shares_prices()
    print(current_prices)
    for uid in [*shares.keys()]:
        price_change = current_prices[uid] / shares[uid]['starting_price']
        if price_change != 1:
            text = await generate_price_changing_text(shares[uid]['name'])
            await bot.send_message(chat_id=config('TG_ID'), text=text)

asyncio.run(get_shares())
asyncio.run(test_check())