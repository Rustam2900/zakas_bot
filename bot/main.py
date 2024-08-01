import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
# from aiogram.utils.i18n import I18n, ConstI18nMiddleware

from bot.config import BOT_TOKEN

from bot.start import router as router_start
# from bot.header.register import router as router_register
# from bot.header.orders import router as router_orders

router = Router()
router.include_router(router_start)
# router.include_router(router_register)
# router.include_router(router_orders)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    db = Dispatcher()

    db.include_router(router)

    await db.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
