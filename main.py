# main.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from utils.scammer_loader import load_scammer_ids
from handlers import start, report, appeal  # 👈 All handlers here

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # ✅ Load scammer list from channel
    await load_scammer_ids(bot)

    # ✅ Register all routers INSIDE main()
    dp.include_router(start.router)
    dp.include_router(report.router)
    dp.include_router(appeal.router)

    # ✅ Start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
