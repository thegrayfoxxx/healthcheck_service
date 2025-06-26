import asyncio

import httpx
from aiogram import Bot

from app.bot import BOT
from app.db import DB
from app.entities import Url
from app.envs import ADMIN_ID, CHECK_URL_BEFORE_NOTIFY


async def send_notify(bot: Bot, chat_id: int, text: str):
    async with bot:
        await bot.send_message(chat_id=chat_id, text=text)


async def check_url(url: Url, timeout: int):
    async with httpx.AsyncClient() as client:
        try:
            await client.get(url.url, timeout=timeout)
            url.status = True
            return url
        except httpx.TimeoutException:
            url.status = False
            return url
        except Exception:
            url.status = False
            return url


async def check_urls(urls: list[Url], timeout: int) -> list[Url]:
    tasks = [check_url(url, timeout) for url in urls]
    return await asyncio.gather(*tasks)


async def check_urls_service(urls: list[Url], timeout: int):
    urls_after_check = await check_urls(urls, timeout)
    for url in urls_after_check:
        if url.status:
            DB.change_url_status(url.url, True)
        else:
            DB.change_url_status(url.url, False)


async def check_urls_loop(delay_loop: int, timeout: int):
    while True:
        urls = DB.get_all_urls()
        await check_urls_service(urls, timeout)
        await asyncio.sleep(delay_loop)


async def notify_loop(delay_loop: int, timeout: int):
    while True:
        bad_urls = DB.get_urls_by_status(False)
        if bad_urls:
            if CHECK_URL_BEFORE_NOTIFY:
                await check_urls_service(bad_urls, timeout)  # type: ignore
                bad_urls = DB.get_urls_by_status(False)
            urls_text = "\n".join([f"{url.url} - {url.status}" for url in bad_urls])  # type: ignore
            await send_notify(
                bot=BOT,
                chat_id=ADMIN_ID,
                text=f"Bad urls:\n{urls_text}",
            )
        await asyncio.sleep(delay_loop)
