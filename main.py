import httpx
import asyncio
from aiogram import Bot
from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def get_env_var(var_name: str) -> str:
    env = getenv(var_name)
    if not env:
        raise ValueError(f"Environment variable {var_name} is not set")
    return env


ADMIN_ID = int(get_env_var("ADMIN_ID"))
BOT_TOKEN = get_env_var("BOT_TOKEN")
DELAY_REQUESTS = int(get_env_var("DELAY_REQUESTS"))
TIMEOUT_REQUESTS = int(get_env_var("TIMEOUT_REQUESTS"))
URLS_LIST = get_env_var("URLS").replace(" ", "").split(",")

bot = Bot(token=BOT_TOKEN)


@dataclass
class Url:
    url: str
    status: bool


async def send_notify(bot: Bot, chat_id: int, text: str):
    async with bot:
        await bot.send_message(chat_id=chat_id, text=text)


async def test_url(url: str) -> Url:
    async with httpx.AsyncClient(verify=False, timeout=TIMEOUT_REQUESTS) as client:
        try:
            await client.get(url)
            return Url(url=url, status=True)
        except httpx.ConnectTimeout:
            return Url(url=url, status=False)
        except Exception:
            return Url(url=url, status=False)


async def test_urls(urls: list[str]) -> list[Url]:
    tasks = [test_url(url) for url in urls]
    return await asyncio.gather(*tasks)


async def bad_urls_process(bad_urls: list[Url]):
    for bad_url in bad_urls:
        await send_notify(
            bot=bot, chat_id=ADMIN_ID, text=f"URL {bad_url.url} is unavailable"
        )


async def main():
    await send_notify(
        bot=bot,
        chat_id=ADMIN_ID,
        text=f"Bot started\n\nHealthcheck urls list:\n{URLS_LIST}",
    )
    while True:
        urls = await test_urls(URLS_LIST)
        bad_urls = [url for url in urls if not url.status]
        await bad_urls_process(bad_urls)
        await asyncio.sleep(DELAY_REQUESTS)


if __name__ == "__main__":
    asyncio.run(main())
