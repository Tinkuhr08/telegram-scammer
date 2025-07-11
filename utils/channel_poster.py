# utils/channel_poster.py

from aiogram import Bot
from config import REPORT_CHANNEL_ID

async def post_report_to_channel(data: dict, bot: Bot, reporter_id: int):
    telegram_id = data.get("telegram_id")
    upi_id = data.get("upi_id") or "❌ Not Provided"
    phone = data.get("phone_number") or "❌ Not Provided"
    amount = data.get("amount")
    image_file_id = data.get("image_file_id")
    proof_file_id = data.get("proof_file_id")

    chat_link = f"tg://openmessage?user_id={telegram_id}"

    text = (
        "🧾 <b>New Scammer Report</b>\n"
        f"<b>Telegram ID:</b> <code>{telegram_id}</code>\n"
        f"<b>UPI:</b> {upi_id}\n"
        f"<b>Phone:</b> {phone}\n"
        f"<b>Amount:</b> ₹{amount}\n"
        f"<b>Chat Link:</b> <a href='{chat_link}'>Click Here</a>\n"
        f"<b>Reported By:</b> <code>{reporter_id}</code>"
    )

    # Send main message
    await bot.send_message(REPORT_CHANNEL_ID, text)

    # Send scammer image if available
    if image_file_id:
        await bot.send_photo(REPORT_CHANNEL_ID, image_file_id, caption="👤 Scammer Image")

    # Send proof (file/photo)
    if proof_file_id:
        try:
            await bot.send_document(REPORT_CHANNEL_ID, proof_file_id, caption="📎 Scam Proof")
        except:
            await bot.send_photo(REPORT_CHANNEL_ID, proof_file_id, caption="📎 Scam Proof (as image)")
