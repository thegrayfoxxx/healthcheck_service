import asyncio



from app.bot import BOT
from app.envs import (
    ADMIN_ID,
    DELAY_NOTIFY_CHECK,
    DELAY_REQUESTS,
    TIMEOUT_BEFORE_NOTIFY_REQUESTS,
    TIMEOUT_REQUESTS,
    URLS_LIST,
)
from app.services import check_urls_loop, notify_loop, send_notify




async def main():
    await send_notify(
        bot=BOT,
        chat_id=ADMIN_ID,
        text=f"Bot started\n\nHealthcheck urls list:\n{URLS_LIST}",
    )
    await asyncio.gather(
        check_urls_loop(DELAY_REQUESTS, TIMEOUT_REQUESTS),
        notify_loop(DELAY_NOTIFY_CHECK, TIMEOUT_BEFORE_NOTIFY_REQUESTS),
    )


if __name__ == "__main__":
    asyncio.run(main())
