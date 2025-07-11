# handlers/report.py

from aiogram import Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from utils.states import ReportScammer
from utils.keyboards import skip_keyboard
from utils.channel_poster import post_report_to_channel

router = Router()

@router.message(Command("report"))
@router.message(Text("🚨 Report Scammer"))
async def report_start(message: types.Message, state: FSMContext):
    await message.answer("🆔 Please send the <b>Telegram ID</b> of the scammer (numeric only):")
    await state.set_state(ReportScammer.telegram_id)

@router.message(ReportScammer.telegram_id)
async def get_telegram_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ Invalid ID. Please enter numeric Telegram ID.")
    await state.update_data(telegram_id=message.text)
    await message.answer("💳 Send UPI ID (or type 'Skip'):", reply_markup=skip_keyboard())
    await state.set_state(ReportScammer.upi_id)

@router.message(ReportScammer.upi_id, F.text)
async def get_upi(message: types.Message, state: FSMContext):
    if message.text.lower() == "skip":
        await state.update_data(upi_id=None)
    else:
        await state.update_data(upi_id=message.text)
    await message.answer("📱 Send Phone Number (or type 'Skip'):", reply_markup=skip_keyboard())
    await state.set_state(ReportScammer.phone_number)

@router.message(ReportScammer.phone_number, F.text)
async def get_phone(message: types.Message, state: FSMContext):
    if message.text.lower() == "skip":
        await state.update_data(phone_number=None)
    else:
        await state.update_data(phone_number=message.text)
    await message.answer("🖼️ Send scammer image (or type 'Skip'):", reply_markup=skip_keyboard())
    await state.set_state(ReportScammer.image)

@router.message(ReportScammer.image, F.photo | F.text)
async def get_image(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "skip":
        await state.update_data(image_file_id=None)
    elif message.photo:
        await state.update_data(image_file_id=message.photo[-1].file_id)
    else:
        return await message.answer("❌ Please send a photo or type 'Skip'")
    
    await message.answer("📎 Send scam proof (image, screenshot, or file):")
    await state.set_state(ReportScammer.proof)

@router.message(ReportScammer.proof, F.photo | F.document)
async def get_proof(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id if message.photo else message.document.file_id
    await state.update_data(proof_file_id=file_id)
    await message.answer("💰 Enter the scam amount in ₹ (numeric only):")
    await state.set_state(ReportScammer.amount)

@router.message(ReportScammer.amount)
async def get_amount(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ Invalid amount. Please enter a number in ₹.")
    
    await state.update_data(amount=message.text)

    data = await state.get_data()
    await state.clear()

    await post_report_to_channel(data, message.bot, reporter_id=message.from_user.id)

    await message.answer("✅ Your report has been submitted successfully. Thank you!")
