from tinkoff.invest import Client

from config.config import load_config

shares = {}
config = load_config()
tinkoff_client = Client(config('TINKOFF_TOKEN'))


async def get_shares(logger):
    with tinkoff_client as client:
        account = client.users.get_accounts().accounts[1]
        account_positions = client.operations.get_portfolio(account_id=account.id).positions
        uid_list = [account_positions[i].instrument_uid for i in range(len(account_positions))]

        for uid in uid_list:
            active = client.instruments.find_instrument(query=uid)
            if active.instruments:
                shares[uid] = {'name': active.instruments[0].name}

        prices = client.market_data.get_last_prices(instrument_id=[*shares.keys()]).last_prices
        for i in range(len(shares)):
            shares[prices[i].instrument_uid]['last_price'] = f'{prices[i].price.units},{prices[i].price.nano}'

        logger.info(shares)
