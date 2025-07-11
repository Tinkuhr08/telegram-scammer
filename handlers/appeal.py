# handlers/appeal.py

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import Text
from utils.states import Appeal
from config import ADMIN_IDS
from aiogram.filters import Command

router = Router()

# 📤 Inline button se start
@router.callback_query(Text("appeal_start"))
async def start_appeal_inline(call: CallbackQuery, state: FSMContext):
    await call.message.answer("📝 Please describe why you are appealing:")
    await state.set_state(Appeal.reason)

# 🛡️ Button se start
@router.message(Text("🛡️ Appeal"))
async def start_appeal_menu(message: types.Message, state: FSMContext):
    await message.answer("📝 Please describe why you are appealing:")
    await state.set_state(Appeal.reason)

@router.message(Appeal.reason)
async def get_reason(message: types.Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await message.answer("📎 Please send any proof (image, screenshot, or document):")
    await state.set_state(Appeal.proof)

@router.message(Appeal.proof, F.photo | F.document)
async def get_proof(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id if message.photo else message.document.file_id
    await state.update_data(proof_file_id=file_id)
    data = await state.get_data()
    await state.clear()

    user_id = message.from_user.id
    chat_link = f"tg://openmessage?user_id={user_id}"

    text = (
        "📤 <b>New Appeal Received</b>\n"
        f"<b>User ID:</b> <code>{user_id}</code>\n"
        f"<b>Reason:</b> {data['reason']}\n"
        f"<b>Chat:</b> <a href='{chat_link}'>Open Chat</a>"
    )

    # Send to all admins privately
    for admin_id in ADMIN_IDS:
        await message.bot.send_message(admin_id, text)
        await message.bot.send_document(admin_id, data['proof_file_id'], caption="📎 Appeal Proof")

    await message.answer("✅ Your appeal has been sent to the admin. They'll review and get back to you.")
