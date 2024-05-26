from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


rmk = ReplyKeyboardRemove()

admin_kb = ReplyKeyboardMarkup(
    keyboard=[[
            KeyboardButton(text="💪 Training starter"),
            KeyboardButton(text='👤 Profile'),
            KeyboardButton(text="⚙️ Admin Panel")
        ]],
        resize_keyboard=True,
    )


admin_panel_kb = ReplyKeyboardMarkup(
    keyboard=[[
            KeyboardButton(text="📤 Mailing"),
            KeyboardButton(text='👨‍💻 User Daten'),
            KeyboardButton(text='📲 Send sms an'),
            KeyboardButton(text="⌨️ Admin kb")
        ]],
        resize_keyboard=True,
    )



user_kb = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="💪 Training starter"),
        KeyboardButton(text='👤 Profile')
    ]], 
    resize_keyboard=True,
)


user_training_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Set hinzufügen"),
            KeyboardButton(text='📋 Training Stats')
        ],
        [
            KeyboardButton(text='❌ Training beenden'),
            KeyboardButton(text='⏱ Timer Starten')
        ]
    ],
    resize_keyboard=True
)