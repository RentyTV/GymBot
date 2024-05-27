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
@router.message(F.text == '⚙️ Admin Panel', IsAdmin(), IsTraining())
async def swap_to_a_panel(message: Message):
    await message.answer('Du bist jetzt im Admin Panel', reply_markup=admin_panel_kb)


@router.message(F.text == '⌨️ Admin kb', IsAdmin(), IsTraining())
async def back_swap_to_a_panel(message: Message):
    await message.answer('Du bist jetzt im Admin Keyboard', reply_markup=admin_kb)

# Profil stats
@router.message(F.text == '👤 Profile', IsAdmin(), IsTraining())
async def profil(message: Message, session: AsyncSession):
    try:
        user = await orm_get_user(session, message.from_user.id)
        if user:
            await message.answer_photo(photo='AgACAgIAAxkBAAPlZlN-v7D4f6nF3nEt3F_by1eO6O4AAvzYMRs0XKBKYKomTD0JEQUBAAMCAAN5AAM1BA', caption=
                    "Hier ist dein Admin Profil\n"
                    "---------------\n"
                    f"🆔: <code>{user.user_id}</code>\n"
                    f"🤩 Name: {user.username}\n"
                    f"🗓 Gym days: {user.g_days}\n"
                    f"🏋️ Gym sets: {user.g_sets}\n"
                    f"⏱ Rest timer: {user.g_timer}\n"
                    f"Registration Zeit: {user.created}", reply_markup=einstellungen)
            # await message.answer(
            #         "Hier ist dein Admin Profil\n"
            #         "---------------\n"
            #         f"🆔: <code>{user.user_id}</code>\n"
            #         f"🤩 Name: {user.username}\n"
            #         f"🗓 Gym days: {user.g_days}\n"
            #         f"🏋️ Gym sets: {user.g_sets}\n"
            #         f"⏱ Rest timer: {user.g_timer}\n"
            #         f"Registration Zeit: {user.created}", reply_markup=einstellungen)
        else:
            await message.answer("User not found")
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}")


# @router.message(F.photo)
# async def photo(message: Message):
#     photo_data = message.photo[-1]
#     await message.answer(f'{photo_data}')


# Mailing to all users
@router.message(StateFilter(None), F.text == '📤 Mailing', IsAdmin(), IsTraining())
async def mailing_command(message: Message, state: FSMContext):
    await message.answer('Gebe mailing sms:')
    await state.set_state(MailForm.message_for_mailing)


@router.message(F.text, MailForm.message_for_mailing, IsAdmin())
async def mailing_command_get(message: Message, state: FSMContext, session: AsyncSession):
    message_text = message.text
    try:
        users = await orm_get_total_users(session)
        i = 0
        for user in users:
            try:
                await send_message_to_user(user.user_id, message_text)
                i = i + 1
            except Exception:
                ...
        await message.answer(f"📤 Mailling war erfolgleich\nHier ist ein text was hat users becomen\n-------------------\n{message_text}\n👤Anzahl des Users: <code>{i}</code>")
    except Exception as e:
        await message.answer(f"Error: {str(e)}")
    await state.clear()


# Check user statistik
class UserSTCheck(StatesGroup):
    get_id_from_user = State()


@router.message(StateFilter(None), F.text == '👨‍💻 User Daten', IsAdmin(), IsTraining())
async def userid_for_st_check_eingabe(message: Message, state: FSMContext):
    await message.answer('Gebe die User ID an:')
    await state.set_state(UserSTCheck.get_id_from_user)


@router.message(F.text, UserSTCheck.get_id_from_user, IsAdmin())
async def userid_for_st_check(message: Message, state: FSMContext, session: AsyncSession):
    id_from_user = message.text
    try:
        user = await orm_get_user(session, int(id_from_user))
        await message.answer(
                    f"Hier ist Stats vom user 🆔: {user.user_id}\n"
                    "---------------\n"
                    f"🤩 Name: {user.username}\n"
                    f"🗓 Gym days: {user.g_days}\n"
                    f"🏋️ Gym sets: {user.g_sets}\n"
                    f"⏱ Rest timer: {user.g_timer}\n"
                    f"Gym status: {user.g_status}\n"
                    f"Registration Zeit: {user.created}")
        await state.clear()
    except Exception as e:
        await message.answer(f"Error: {str(e)}")
    await state.clear()


@router.message(F.text == '/alist', IsAdmin())
async def get_list_of_users(message: Message, session: AsyncSession):
    try:
        users = await orm_get_total_users(session)
        i = 0
        user_list = []
        for user in users:
            i = i + 1
            username, user_id = user.username, user.user_id
            user_list.append(f"User_name: {username} | User_id: {user_id}")
        final_output = '\n'.join(user_list)
        await message.answer(f'Anzahl des users: {i}\n--------------------\n{final_output}\n')
    except Exception as e:
        await message.answer(f"Error: {str(e)}")


# Send sms an use
class Sendsms(StatesGroup):
    get_id_from_user = State()
    sms_from_admin = State()


@router.message(StateFilter(None), F.text == '📲 Send sms an', IsAdmin(), IsTraining())
async def sms_send_anfang(message: Message, state: FSMContext):
    await message.answer('Gebe die User ID an:')
    await state.set_state(Sendsms.get_id_from_user)


@router.message(F.text, Sendsms.get_id_from_user, IsAdmin())
async def sms_send_user_id_check(message: Message, state: FSMContext, session: AsyncSession):
    id_from_user = int(message.text)
    try:
        user = await orm_get_user(session, id_from_user)
        if user:
            await state.update_data(user_id=id_from_user)
            await message.answer('Gebe die SMS an:')
            await state.set_state(Sendsms.sms_from_admin)
        else:
            await message.answer("Falsche Benutzer-ID")
    except Exception as e:
            await message.answer(f"Error: {str(e)}")


@router.message(F.text, Sendsms.sms_from_admin, IsAdmin())
async def sms_send_to_user_finish(message: Message, state: FSMContext, session: AsyncSession):
    sms_to_send = str(message.text)
    data = await state.get_data()
    try:
        await send_message_to_user(int(data['user_id']), sms_to_send)
        await message.answer(f'Du hast gesendet an user mit ID: <b>{int(data['user_id'])}</b>\n-----------\nText: <code>{sms_to_send}</code>')
        await state.clear()
    except Exception as e:
            await message.answer(f"Error: {str(e)}")
