# handlers/start.py

from aiogram import Router, types
from aiogram.filters import CommandStart
from global_data.scammer_cache import SCAMMER_IDS
from utils.keyboards import appeal_button, main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def handle_start(message: types.Message):
    user_id = message.from_user.id

    if user_id in SCAMMER_IDS:
        text = (
            "⚠️ <b>Aap is bot mein as a scammer listed hain.</b>\n\n"
            "Aap is bot ke features use nahi kar sakte. Agar aapko lagta hai ki galat report hua hai, "
            "to neeche Appeal button dabayein."
        )
        await message.answer(text, reply_markup=appeal_button())
    else:
        await message.answer("👋 <b>Welcome to Scammer Buster Bot!</b>", reply_markup=main_menu_keyboard())
