from tinkoff.invest import Client

from config.config import load_config

config = load_config()
tinkoff_client = Client(config('TINKOFF_TOKEN'))

with tinkoff_client as client:
    print(client.users.get_accounts())
