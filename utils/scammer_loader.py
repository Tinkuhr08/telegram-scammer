# utils/scammer_loader.py

from aiogram import Bot
from global_data.scammer_cache import SCAMMER_IDS
import re

# Yeh teri private channel ID honi chahiye (jaise: -1001234567890)
SCAMMER_CHANNEL_ID = -2561349129  # <- isko tu apne channel ID se replace kare

# Scam message se Telegram ID extract karne ke liye regex
ID_PATTERN = re.compile(r"Telegram ID:\s*(\d+)", re.IGNORECASE)

async def load_scammer_ids(bot: Bot):
    SCAMMER_IDS.clear()
    offset_id = 0
    limit = 100

    while True:
        history = await bot.get_chat_history(SCAMMER_CHANNEL_ID, offset_id=offset_id, limit=limit)
        messages = history.messages

        if not messages:
            break

        for msg in messages:
            match = ID_PATTERN.search(msg.text or "")
            if match:
                telegram_id = int(match.group(1))
                SCAMMER_IDS.add(telegram_id)

        offset_id = messages[-1].message_id

    print(f"[LOADED] Total scammers found: {len(SCAMMER_IDS)}")
