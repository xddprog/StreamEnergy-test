import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
from config import load_bot_token
from middlewares.auth_middleware import AuthCheckMiddleware


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    bot_token = load_bot_token()

    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.outer_middleware(AuthCheckMiddleware())

    dp.include_router(handlers.auth_router)
    dp.include_router(handlers.tasks_router)
    dp.include_router(handlers.menu_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
