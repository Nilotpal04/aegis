import asyncio

import httpx


URLS = [
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:8001/",
]


async def send_request(client: httpx.AsyncClient, url: str):
    response = await client.get(url)
    print(url, response.status_code)


async def main():
    async with httpx.AsyncClient() as client:
        tasks = []

        for _ in range(10):
            for url in URLS:
                tasks.append(send_request(client, url))

        await asyncio.gather(*tasks)


asyncio.run(main())