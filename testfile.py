import asyncio
from tinkoff.invest import AsyncClient

async def main():
    async with AsyncClient('t.25xAhNNor6Jt3HcA1tvavFwFhLaPCPT6nuOEBeIYmkBzcOSlxGIwI17auX27L4RiUQQMsQNwkkKtYGHOm9Q0MA') as client:
        accounts = await client.users.get_accounts()
        a = accounts.accounts[1]
        print(accounts)


if __name__ == "__main__":
    asyncio.run(main())
