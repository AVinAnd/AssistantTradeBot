from aiogram import Bot
from tinkoff.invest import AsyncClient

from config.config import load_config
from lexicon.lexicon import generate_price_changing_text

shares = {}
config = load_config()
bot = Bot(token=config('BOT_TOKEN'))


async def get_shares(logger):
    async with AsyncClient(config('TINKOFF_TOKEN')) as client:
        accounts = await client.users.get_accounts()
        account = accounts.accounts[1]
        account_positions_list = await client.operations.get_portfolio(
            account_id=account.id
        )
        account_positions = account_positions_list.positions
        uid_list = [account_positions[i].instrument_uid
                    for i in range(len(account_positions))]

        for uid in uid_list:
            active = await client.instruments.find_instrument(query=uid)
            if active.instruments:
                shares[uid] = {'name': active.instruments[0].name}

        await update_prices()
        logger.info(shares)


async def get_shares_prices() -> dict:
    current_prices = {}
    async with AsyncClient(config('TINKOFF_TOKEN')) as client:
        prices_list = await client.market_data.get_last_prices(
            instrument_id=[*shares.keys()]
        )
        prices = prices_list.last_prices
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
        if not 0.98 < price_change < 1.02:
            text = await generate_price_changing_text(shares[uid]['name'])
            await bot.send_message(chat_id=config('TG_ID'), text=text)


async def update_prices():
    current_prices = await get_shares_prices()
    for uid in current_prices.keys():
        shares[uid]['starting_price'] = current_prices[uid]
