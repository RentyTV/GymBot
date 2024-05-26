import asyncio
import random
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from config_reader import config

from db.orm_query import (
    orm_add_user_sets, orm_add_user_training, orm_check_user_sets,
    orm_get_user, orm_get_user_set, orm_get_user_training_via_data,
    orm_update_user, orm_update_user_sets
)
from filters.is_admin import IsAdmin
from keyboards.inline import *
from keyboards.reply import admin_kb, user_kb, user_training_kb


router = Router()
current_date = datetime.now().date()
# current_date = current_date_1.strftime("%Y-%m-%d")


@router.message(F.text == '👤 Profile')
async def profile(message: Message, session: AsyncSession):
    try:
        user = await orm_get_user(session, message.from_user.id)
        if user:
            if not user.g_status:
                await message.answer_photo(photo='AgACAgIAAxkBAAPlZlN-v7D4f6nF3nEt3F_by1eO6O4AAvzYMRs0XKBKYKomTD0JEQUBAAMCAAN5AAM1BA', caption=
                    "Hier ist dein Profil\n"
                    "---------------\n"
                    f"🆔: <code>{user.user_id}</code>\n"
                    f"🤩 Name: {user.username}\n"
                    f"🗓 Gym days: {user.g_days}\n"
                    f"🏋️ Gym sets: {user.g_sets}\n"
                    f"⏱ Rest timer: {user.g_timer}\n"
                    f"Registration Zeit: {user.created}", reply_markup=einstellungen)
            else:
                await message.answer("Du trainierst bereits")
        else:
            await message.answer("User not found")
    except Exception as e:
        await message.answer(f"Error: \n{str(e)}")


# Einstellungen actionen
@router.callback_query(F.data == "einstellungen")
async def einstellungen_start(callback: CallbackData):
    await callback.message.delete()
    await callback.message.answer('Hier sind deine Einstellungen.\n--------------\nMöchtest du wirklich die Timer-Zeit ändern?', reply_markup = einstellungen_frage)


# Einstellungen FSM start
class Einstell(StatesGroup):
    time = State()


@router.callback_query(F.data.startswith("einstell_"))
async def einstellungen_fortsetz(callback: CallbackData, state: FSMContext):
    await callback.message.delete()
    if F.data == 'einstell_yes':
        await callback.message.answer('Eingabe der Timerzeit im Format x.x (sekunden)')
        await state.set_state(Einstell.time)
    else: 
        await callback.message.answer('Okey')


@router.message(Einstell.time, F.text)
async def einstellungen_fortsetz_1(message: Message, state: FSMContext, session: AsyncSession):
    try:
        time = float(message.text)
        await orm_update_user(session, message.from_user.id, g_timer=time)
        if message.from_user.id in config.ADMIN_IDS:
            await message.answer(f'Die Zahl: {time} wurde beibehalten.', reply_markup=admin_kb)
        else:
            await message.answer(f'Die Zahl: {time} wurde beibehalten.', reply_markup=user_kb)
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}")



# Training starter handler
@router.message(F.text == '💪 Training starter')
async def training_start(message: Message, session: AsyncSession):
    try:
        user = await orm_get_user(session, message.from_user.id)
        if not user.g_status:
            training_check = await orm_get_user_training_via_data(session, user_id=message.from_user.id, created_date=current_date)
            if training_check is None:
                await orm_add_user_training(session, message.from_user.id)
                await asyncio.sleep(0.3)
                training = await orm_get_user_training_via_data(session, message.from_user.id, current_date) 
                await message.answer('Welche Muskeln möchtest du heute trainieren?', reply_markup=traning_frage(training))
            else:
                await message.answer('1 Tag - 1 Training. Du darfst nicht mehr Trainieren!')
        else: 
            await message.answer('Du trainierst bereits.')
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}")


@router.callback_query(WahlAction.filter())
async def training_n_start(callback: CallbackQuery, callback_data: WahlAction, session: AsyncSession):
    try:
        training = await orm_get_user_training_via_data(session, callback.from_user.id, current_date)
        act = str(callback_data.action)
        if act != 'confirm':
            if getattr(training, act) is not True:
                setattr(training, act, True)
                await session.commit()
                await callback.message.delete()
                await callback.message.answer(
                    f'Was noch?\n--------------\nÄnderungen\n{act.capitalize()}: ✅ True',
                    reply_markup=traning_frage(training)
                )
            else:
                setattr(training, act, False)
                await session.commit()
                await callback.message.delete()
                await callback.message.answer(
                    f'Was noch?\n--------------\nÄnderungen\n{act.capitalize()}: ❌ False',
                    reply_markup=traning_frage(training)
                )
        elif act == 'confirm':
            if any([value for value in training.__dict__.values() if isinstance(value, bool) and value]):
                    await callback.message.delete()
                    await orm_update_user(session, callback.from_user.id, g_status=True)
                    await callback.message.answer('Das Training hat begonnen', reply_markup=user_training_kb)

    except Exception as e:
        await callback.message.answer(
            f"Error: \n{str(e)}")


# Training Stats handler
@router.message(F.text == '📋 Training Stats')
async def training_stats(message: Message, session: AsyncSession):
    try:
        user = await orm_get_user_training_via_data(session, message.from_user.id, current_date)
        response = f"Hier ist dein Training Stats\n---------------\nHeute machts du:\n"
        attributes = ['arme', 'rucken', 'bauch', 'beine', 'brust']
        for attribute in attributes:
            if getattr(user, attribute):
                response += f"<code>{attribute.capitalize()}</code>\n"
        sets_attributes = ['arme_sets', 'rucken_sets', 'bauch_sets', 'beine_sets', 'brust_sets']
        for sets_attribute in sets_attributes:
            sets_value = getattr(user, sets_attribute)
            if sets_value > 0:
                response += f"<code>{sets_attribute.capitalize()}: {sets_value}</code>\n"
        await message.answer(response)
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}")


# Training Stats handler
@router.message(F.text == '❌ Training beenden')
async def training_end(message: Message, session: AsyncSession):
    try:
        user = await orm_get_user(session, message.from_user.id)
        if user.g_status == True: 
            await orm_update_user(session, message.from_user.id, g_status=False, g_days=user.g_days + 1)
            # await orm_update_user_status(session, message.from_user.id, g_status=False)
            if message.from_user.id in config.ADMIN_IDS:
                await message.answer('Dein Training ist abgeschlossen', reply_markup=admin_kb)
            else:
                await message.answer('Dein Training ist abgeschlossen', reply_markup=user_kb)
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}")


# Training set hinzufügen
class Sset(StatesGroup):
    notiz = State()
    repetitions = State()


@router.message(StateFilter(None), F.text == '➕ Set hinzufügen')
async def make_new_set(message: Message, state: FSMContext):
    try:
        # user_training_data = await orm_get_user_training_via_data(session, created_date=current_date)
        await message.answer('Schreiben Sie hier eine Notiz oder den Namen des Ansatzes')
        await state.set_state(Sset.notiz)
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}")


@router.message(Sset.notiz, F.text)
async def make_new_set_s1(message: Message, state: FSMContext):
    try:
        await state.update_data(notiz=message.text)
        await message.answer('Wie viele Sätze hast du gemacht?')
        await state.set_state(Sset.repetitions)
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}")


async def check_user_sets(session, message):
    random_n = random.randint(0,10000000)
    my_str = str(message.from_user.id) + '_' + str(random_n)
    if await orm_check_user_sets(session, my_str):
        return False
    else:
        return my_str


@router.message(Sset.repetitions, F.text)
async def make_new_set_s2(message: Message, state: FSMContext, session: AsyncSession):
    try:
        repetitions_from_user = int(message.text)
        data = await state.get_data()
        check = await check_user_sets(session, message)
        if not check:
            await message.answer('es hat sich verdoppelt')
            check2 = await check_user_sets(session, message)
            await orm_add_user_sets(session, check2, message.from_user.id, 'None', str(data['notiz']), None)
            user_training_data = await orm_get_user_training_via_data(session, message.from_user.id, current_date)
            await message.answer('Wählen Sie aus, für welchen Körperteil Sie einen Satz gemacht haben', reply_markup=sset_create(user_training_data, check2, repetitions_from_user))
        else:
            await orm_add_user_sets(session, check, message.from_user.id, 'None', str(data['notiz']), None)
            user_training_data = await orm_get_user_training_via_data(session, message.from_user.id, current_date)
            await message.answer('Wählen Sie aus, für welchen Körperteil Sie einen Satz gemacht haben', reply_markup=sset_create(user_training_data, check, repetitions_from_user))
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}")


@router.callback_query(Sset_Add.filter())
async def make_new_set_s3(callback: CallbackQuery, callback_data: Sset_Add, session: AsyncSession):
    act = str(callback_data.set_action)
    set_id = callback_data.set_id
    rps = callback_data.repetitions
    await callback.message.delete()
    try:
        user = await orm_get_user(session, callback.from_user.id)
        await orm_update_user(session, callback.from_user.id, g_sets=user.g_sets + 1)
        current_training = await orm_get_user_training_via_data(session, callback.from_user.id, current_date)
        setattr(current_training, act, getattr(current_training, act) + 1)
        # await orm_update_user_training(session, current_date, act=getattr(current_training, act) + 1)
        await orm_update_user_sets(session, set_id, muskul_typ=act, repetitions=rps)
        current_set = await orm_get_user_set(session, set_id)
        await callback.message.answer(f'Dein set\n------------\nAction: {act}\nDeine Notiz: {current_set.notiz}\nDie Anzahl der Wiederholungen: {rps}')
    except Exception as e:
        await callback.message.answer(
            f"Error: \n{str(e)}")


@router.message(F.text == '⏱ Timer Starten')
async def timer_starten(message: Message, session: AsyncSession):
    user = await orm_get_user(session, message.from_user.id)
    await message.answer(f"Ihr Timer hat begonnen. Timer-Zeit:{user.g_timer}")
    await asyncio.sleep(user.g_timer)
    await message.answer(f"Ihr Timer ist abgelaufen. Timer-Zeit:{user.g_timer}")