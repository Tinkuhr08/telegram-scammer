# utils/keyboards.py

from aiogram.types import 
InlineKeyboardMarkup,
InlineKeyboardButton,
ReplyKeyboardMarkup, 
KeyboardButton

def appeal_button():
    return
  InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Appeal Now", 
                              callback_data="appeal_start")]
    ])

def main_menu_keyboard():
    buttons = [
        [KeyboardButton(text="🔍 Check Scammer")],
        [KeyboardButton(text="🚨 Report Scammer")],
        [KeyboardButton(text="📊 Top Scammers"), KeyboardButton(text="🧾 My Reports")]
    ]
    return 
  ReplyKeyboardMarkup(keyboard=buttons,
                      resize_keyboard=True)
