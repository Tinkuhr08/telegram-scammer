# main.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from utils.scammer_loader import load_scammer_ids
from handlers import start  # we'll add more handlers later

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # ✅ Load scammer IDs on startup
    await load_scammer_ids(bot)

    # ✅ Register handlers
    dp.include_router(start.router)

    # ✅ Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
