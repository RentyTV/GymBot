from aiogram import Router, F
from aiogram.filters import StateFilter, or_f
from aiogram.types import Message
from filters.is_admin import IsAdmin
from keyboards.reply import admin_panel_kb, admin_kb
from keyboards.inline import einstellungen
from db.orm_query import orm_get_total_users, orm_get_user
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from __main__ import send_message_to_user
from filters.is_training import IsTraining

router = Router()

class MailForm(StatesGroup):
    message_for_mailing = State()

# Swap to admin panel kb and reverce
@router.message(F.text == 'Admin Panel', IsAdmin(), IsTraining())
async def swap_to_a_panel(message: Message):
    await message.answer('Du bist jetzt im Admin Panel', reply_markup=admin_panel_kb)


@router.message(F.text == 'Admin kb', IsAdmin(), IsTraining())
async def back_swap_to_a_panel(message: Message):
    await message.answer('Du bist jetzt im Admin Keyboard', reply_markup=admin_kb)

# Profil stats
@router.message(F.text == 'Profile', IsAdmin(), IsTraining())
async def profil(message: Message, session: AsyncSession):
    try:
        user = await orm_get_user(session, message.from_user.id)
        if user:
            await message.answer(f"Hier ist dein Admin Profil\n---------------\nDein ID: <code>{user.user_id}</code>\nUser name: {user.username}\nGym days: {user.g_days}\nGym sets: {user.g_sets}\nRest timer: {user.g_timer}\nRegistration Zeit: {user.created}", reply_markup=einstellungen)
        else:
            await message.answer("User not found")
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}")

# Mailing to all users
@router.message(StateFilter(None), F.text == 'Mailing', IsAdmin(), IsTraining())
async def mailing_command(message: Message, state: FSMContext):
    await message.answer('Gebe mailing sms')
    await state.set_state(MailForm.message_for_mailing)


@router.message(F.text, MailForm.message_for_mailing, IsAdmin())
async def mailing_command_get(message: Message, state: FSMContext, session: AsyncSession):
    message_text = message.text
    try:
        users = await orm_get_total_users(session)
        for user in users:
            await send_message_to_user(user.user_id, message_text)
        await message.answer(f"Mailling war erfolgleich\nHier ist ein text was hat user becomen\n-------------------\n{message_text}")
    except Exception as e:
        await message.answer(f"Error: {str(e)}")
    await state.clear()
