from tinkoff.invest import Client

from config.config import load_config

shares = {}
config = load_config()
tinkoff_client = Client(config('TINKOFF_TOKEN'))


with tinkoff_client as client:
    account = client.users.get_accounts().accounts[1]
    account_positions = client.operations.get_portfolio(account_id=account.id).positions
    uid_list = [account_positions[i].instrument_uid for i in range(len(account_positions))]
    for uid in uid_list: #def1
        active = client.instruments.find_instrument(query=uid)
        if active.instruments:
            shares[uid] = {'name': active.instruments[0].name}

    prices = client.market_data.get_last_prices(instrument_id=[*shares.keys()])
    for i in range(len(shares)): #def2
        shares[prices.last_prices[i].instrument_uid]['price'] = f'{prices.last_prices[i].price.units},{prices.last_prices[i].price.nano}'

    print(shares)
